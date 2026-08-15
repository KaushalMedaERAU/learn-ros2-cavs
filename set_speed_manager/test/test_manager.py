import pytest
from set_speed_manager.manager import SetSpeedManager


@pytest.fixture
def speed_setpoint():
    return SetSpeedManager()


@pytest.mark.req('SSM-FR-001')
def test_initial_set_speed(speed_setpoint):
    assert speed_setpoint.speed_mph == 0


@pytest.mark.req('SSM-FR-005')
@pytest.mark.parametrize(
    'speed, expected',
    [
        pytest.param(-5, 0, id='below-minimum', marks=pytest.mark.req('SSM-FR-004')),
        pytest.param(0, 0, id='minimum'),
        pytest.param(15, 15, id='normal'),
        pytest.param(65, 65, id='maximum'),
        pytest.param(70, 65, id='above-maximum', marks=pytest.mark.req('SSM-FR-004')),
    ],
)
def test_speed_setting(speed_setpoint, speed, expected):
    speed_setpoint.set_speed(speed)
    assert speed_setpoint.speed_mph == expected


@pytest.mark.req('SSM-FR-002')
@pytest.mark.parametrize(
        'speed, expected',
        [
            pytest.param(15, 20, id='normal'),
            pytest.param(60, 65, id='maxiumum'),
            pytest.param(65, 65, id='above-maximum', marks=pytest.mark.req('SSM-FR-004'))
        ]
)
def test_speed_increment(speed_setpoint, speed, expected):
    speed_setpoint.set_speed(speed)
    speed_setpoint.increment_speed()
    assert speed_setpoint.speed_mph == expected


@pytest.mark.req('SSM-FR-003')
@pytest.mark.parametrize(
        'speed, expected',
        [
            pytest.param(15, 10, id='normal'),
            pytest.param(5, 0, id='minimum'),
            pytest.param(0, 0, id='below-minimum', marks=pytest.mark.req('SSM-FR-004'))
        ]
)
def test_speed_decrement(speed_setpoint, speed, expected):
    speed_setpoint.set_speed(speed)
    speed_setpoint.decrement_speed()
    assert speed_setpoint.speed_mph == expected
