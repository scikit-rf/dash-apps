# Jackson Anderson
import json
import numpy as np
import skrf as rf
from os.path import join, realpath, pardir, abspath


# from hypothesis import given, strategies as st
# from hypothesis.extra import numpy as stnp


# unit_dict = { \
#     'hz': 'Hz', \
#     'khz': 'KHz', \
#     'mhz': 'MHz', \
#     'ghz': 'GHz', \
#     'thz': 'THz' \
#     }
# datatypes = st.one_of(st.integers,st.floats,st.complex_numbers)
# # TODO: fix arguements for st.builds so that it generates correctly
#
# def build_hypothesis_test_network(nports, npoints):
#     return st.builds(
#         rf.Network,
#         name=st.characters,
#         f=stnp.arrays(datatypes, [npoints]),
#         z0=stnp.arrays(datatypes, [st.sampled_from([nports, npoints])]),
#         s=stnp.arrays(datatypes, [npoints, nports, nports]),
#         comments=st.characters,
#         f_unit=st.sampled_from((None, 'hz', 'khz', 'mhz', 'ghz'))
#     )

# test_ntwk = build_hypothesis_test_network(st.integers(min_value=1, max_value=20),
#                                           st.integers(min_value=0, max_value=100000))
#
#
# @given(test_ntwk)
# def test_random_snp(obj):
#     assert False


class TouchstoneEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.complex):
            return np.real(obj), np.imag(obj)  # split into [real, im]
        if isinstance(obj, rf.Frequency):
            return {'flist': obj.f_scaled.tolist(), 'funit': obj.unit}
        return json.JSONEncoder.default(self, obj)


def to_json(network):
    return json.dumps(network.__dict__, cls=TouchstoneEncoder)


def from_json(obj_string):
    obj = json.loads(obj_string)
    ntwk = rf.Network()
    ntwk.variables = obj['variables']
    ntwk.name = obj['name']
    ntwk.comments = obj['comments']
    ntwk.port_names = obj['port_names']
    ntwk.z0 = np.array(obj['_z0'])[..., 0] + np.array(obj['_z0'])[..., 1] * 1j  # recreate complex numbers
    ntwk.s = np.array(obj['_s'])[..., 0] + np.array(obj['_s'])[..., 1] * 1j
    ntwk.frequency = rf.Frequency.from_f(np.array(obj['_frequency']['flist']),
                                         unit=obj['_frequency']['funit'])
    return ntwk


def test_snp_json_roundtrip():
    '''
    Tests if snp object saved to json and reloaded is still the same.
    :return:
    '''
    datafile = r'357_pcb_960978_um_pe_001_25.s3p'
    rootdir = abspath(join(realpath(__file__), pardir, pardir))
    given = rf.Network(join(rootdir, 'example_data', datafile))
    actual = from_json(to_json(given))
    assert actual == given
    assert actual.frequency == given.frequency
    assert actual.name == given.name

