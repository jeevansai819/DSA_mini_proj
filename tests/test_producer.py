"""
Unit tests for Scenario Generator and Event formatting.
"""
import pytest
from simulation.scenario_generator import ScenarioGenerator

def test_scenario_generator_modes():
    gen = ScenarioGenerator()
    
    # Test Normal Traffic Mode
    gen.set_mode("NORMAL_TRAFFIC")
    event = gen.generate_event()
    assert event["event_type"] == "NORMAL"
    assert event["average_speed"] >= 60.0
    assert "event_id" in event
    assert "timestamp" in event
    
    # Test Accident Scenario Mode
    target = "Highway-101-North"
    gen.set_mode("ACCIDENT_SCENARIO", target_location=target)
    # Generate until matching target location
    for _ in range(10):
        ev = gen.generate_event()
        if ev["location"] == target:
            assert ev["event_type"] == "SIMULATED_ACCIDENT"
            assert ev["average_speed"] <= 25.0
            break
            
    # Reset
    gen.set_mode("NORMAL_TRAFFIC")
