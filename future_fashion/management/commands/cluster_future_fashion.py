from __future__ import unicode_literals, absolute_import, print_function, division

import numpy
from scipy.cluster.vq import kmeans2

from core.management.commands._community import CommunityCommand
from core.utils.configuration import DecodeConfigAction


def cast_elements_to_floats(lst):
    return [float(flt) for flt in lst]


class Command(CommunityCommand):

    def add_arguments(self, parser):
        parser.add_argument('community', type=str, nargs="?", default="FutureFashionCommunity")
        parser.add_argument('-c', '--config', type=str, action=DecodeConfigAction, nargs="?", default={})

    def get_community(self):
        community, created = self.model.objects.get_latest_or_create_by_signature("kleding", **self.config)
        return community

    def handle_community(self, community, **options):
        clothing_vectors = numpy.array([
            cast_elements_to_floats(individual["vectors"]) for individual in community.kernel.individual_set.all()
        ])
        centroids, labels = kmeans2(clothing_vectors, 10, minit="points")
        import ipdb; ipdb.set_trace()