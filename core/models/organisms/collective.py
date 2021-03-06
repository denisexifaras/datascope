from __future__ import unicode_literals, absolute_import, print_function, division
import six

from collections import Iterator, Iterable

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

import json_field
from json_field.fields import JSONEncoder, JSONDecoder

from core.models.organisms import Organism, Individual
from core.utils.helpers import ibatch
from core.utils.data import reach


class IndexEncoder(JSONEncoder):
    def encode(self, obj):
        obj = super(IndexEncoder, self).encode({str(value): key for key, value in six.iteritems(obj)})
        return obj


class IndexDecoder(JSONDecoder):
    def decode(self, obj, *args, **kwargs):
        obj = super(IndexDecoder, self).decode(obj, *args, **kwargs)
        return {key: int(value) for value, key in six.iteritems(obj)}


class Collective(Organism):  # TODO: rename to family

    indexes = json_field.JSONField(
        null=True,
        blank=True,
        default={},
        encoder=IndexEncoder,
        decoder=IndexDecoder
    )
    identifier = models.CharField(max_length=255, null=True, blank=True)

    @property
    def url(self):
        if not self.id:
            raise ValueError("Can't get url for unsaved Collective")
        return reverse("v1:collective-content", args=[self.id])  # TODO: make version aware

    @staticmethod
    def validate(data, schema):
        """
        Validates the data against given schema for one of more Individuals.

        :param data: The data to validate
        :param schema: The JSON schema to use for validation.
        :return: Valid data
        """
        if not isinstance(data, Iterable):
            data = [data]
        for instance in data:
            Individual.validate(instance, schema)

    def update(self, data, validate=True, reset=True, batch_size=500):  # TODO: rename to "add" and implement "update"
        """
        Update the instance with new data by adding to the Collective
        or by updating Individuals that are on the Collective.

        :param data: The data to use for the update
        :param validate: (optional) whether to validate data or not (yes by default)
        :return: A list of updated or created instances.
        """
        assert isinstance(data, (Iterator, list, tuple, dict, Individual)), \
            "Collective.update expects data to be formatted as iteratable, dict or Individual not {}".format(type(data))

        if reset:
            self.individual_set.all().delete()

        def prepare_updates(data):

            prepared = []
            if isinstance(data, dict):
                if validate:
                    Individual.validate(data, self.schema)
                individual = Individual(
                    community=self.community,
                    collective=self,
                    schema=self.schema,
                    properties=data
                )
                individual.clean()
                prepared.append(individual)
            elif isinstance(data, Individual):
                if validate:
                    Individual.validate(data, self.schema)
                data.id = None
                data.collective = self
                data.clean()
                prepared.append(data)
            else:  # type is list
                for instance in data:
                    prepared += prepare_updates(instance)
            return prepared

        update_count = 0
        for updates in ibatch(data, batch_size=batch_size):
            updates = prepare_updates(updates)
            update_count += len(updates)
            Individual.objects.bulk_create(updates, batch_size=settings.MAX_BATCH_SIZE)

        return update_count

    @property
    def content(self):
        """
        Returns the content of the members of this Collective

        :return: a generator yielding properties from Individual members
        """
        return (ind.content for ind in self.individual_set.iterator())

    @property
    def has_content(self):
        """
        Indicates if Collective entails Individuals or not

        :return: True if there are Individuals, False otherwise
        """
        return self.individual_set.exists()

    @property
    def json_content(self):
        json_content = [ind.json_content for ind in self.individual_set.all()]
        return "[{}]".format(",".join(json_content))

    def output(self, *args):
        if len(args) > 1:
            return map(self.output, args)
        frm = args[0]
        if not frm:
            return [frm for ind in range(0, self.individual_set.count())]
        elif isinstance(frm, list):
            output = self.output(*frm)
            if len(frm) > 1:
                output = [list(zipped) for zipped in zip(*output)]
            else:
                output = [[out] for out in output]
            return output
        else:
            return [ind.output(frm) for ind in self.individual_set.iterator()]

    def group_by(self, key):
        """
        Outputs a dict with lists. The lists are filled with Individuals that hold the same value for key.

        :param key:
        :return:
        """
        grouped = {}
        for ind in self.individual_set.all():
            assert key in ind.properties, \
                "Can't group by {}, because it is missing from an individual on collective {}".format(key, self.id)
            value = ind.properties[key]
            if value not in grouped:
                grouped[value] = [ind]
            else:
                grouped[value].append(ind)
        return grouped

    def _get_index_keys(self):
        return [item[0] for item in next(six.iterkeys(self.indexes))]

    def build_index(self, keys):
        """

        :param keys:
        :return:
        """
        assert isinstance(keys, list) and len(keys), \
            "Expected a list with at least one element for argument keys."

        individuals = []
        for ind in self.individual_set.all():
            self.set_index_for_individual(ind, keys)
            individuals.append(ind)
        self.update(individuals)
        self.save()

    def set_index_for_individual(self, individual, index_keys):
        index = tuple([(key, individual[key]) for key in index_keys])
        if index not in self.indexes:
            index_code = len(self.indexes)
            self.indexes[index] = index_code
        individual.index = self.indexes[index]
        return individual

    def influence(self, individual):
        """
        This allows the Collective to set some attributes and or properties on the Individual

        :param individual: The individual that should be influenced
        :return: The influenced individual
        """
        if self.identifier:
            individual.identity = reach("$." + self.identifier, individual.properties)
        if self.indexes:
            index_keys = self._get_index_keys()
            individual = self.set_index_for_individual(individual, index_keys)

        return individual

    def select(self, **kwargs):
        select = set()
        for item in six.iteritems(kwargs):
            for index in self.indexes.keys():
                if item in index:
                    select.add(self.indexes[index])
        return self.individual_set.filter(index__in=select)
