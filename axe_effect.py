
from .agent_based_api.v1 import (
    register,
    Result,
    Service,
    startswith,
    SNMPTree,
    State,
    Metric,
    ServiceLabel,
)

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .utils.temperature import (
    check_temperature,
)

from .utils.humidity import (
    check_humidity,
)




def parse_axe(string_table):
    result = {}
    result['temperature'] = float(string_table[0][0]) / 100
    result['humidity'] = float(string_table[0][1]) / 1000
    return result




def discover_axe(section, params, sfunc) -> DiscoveryResult:
    yield Service(
        item='Temperature',
        parameters={},
       # labels=[ ServiceLabel('test3', "test4") ]
    )

    yield Service(
        item='Humidity',
        parameters={},
       # labels=[ ServiceLabel('test3', "test4") ]
    )



def check_axe_effect(item='', params=None, section=None):
    if (item == 'Temperature'):
        yield from check_temperature(
            section['temperature'],
            params,
            dev_levels=(31, 37),
            dev_levels_lower=(10, 10),
            dev_status=State.OK,
        )


    if (item == 'Humidity'):
        yield from check_humidity(
            section['humidity'],
            params,
        )




register.snmp_section(
    name = 'axe_effect_snmp',
    parse_function = parse_axe,
    detect = startswith('.1.3.6.1.2.1.1.1.0', 'AxeEffect'),
    fetch = SNMPTree(base='.1.3.6.1.2.1.99.1.1', oids=['1.4', '2.4']),
)




register.check_plugin(
    name = 'axe_effect',
    sections = ['axe_effect_snmp'],
    service_name = 'Tempie McSensorface %s',
    discovery_function=lambda section: (
        yield from discover_axe(section, {}, 'temp')
    ),
    check_function = check_axe_effect,
    check_ruleset_name='temperature',
    check_default_parameters={},
)
