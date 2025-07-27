import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_critical_power(power_1, time_1, power_2, time_2):
    """
    Calculate critical power using two all-out efforts with power and time.
    
    Parameters:
    power_1 (float): Average power in trial 1 (W)
    time_1 (float): Time for trial 1 (seconds)
    power_2 (float): Average power in trial 2 (W)
    time_2 (float): Time for trial 2 (seconds)
    
    Returns:
    float: critical power (W)
    """
    if time_1 == time_2:
        return None  # Avoid division by zero
    return (power_1 * time_1 - power_2 * time_2) / (time_1 - time_2)


def main():
    st.title("Critical Power Calculator (Two-Point Model, Power-Based)")
    st.write("Calculate your critical power based on two all-out efforts using distance, time, and power.")
    
    # Input fields
    st.subheader("Trial 1")
    distance_1 = st.number_input(
        "Distance for Trial 1 (meters)", 
        min_value=0.0, 
        max_value=100000.0, 
        value=1000.0,
        step=1.0
    )
    time_1 = st.number_input(
        "Time for Trial 1 (seconds)", 
        min_value=1.0, 
        max_value=100000.0, 
        value=240.0,
        step=1.0
    )
    power_1 = st.number_input(
        "Average Power for Trial 1 (Watts)",
        min_value=0.0,
        max_value=2000.0,
        value=300.0,
        step=1.0
    )
    
    st.subheader("Trial 2")
    distance_2 = st.number_input(
        "Distance for Trial 2 (meters)", 
        min_value=0.0, 
        max_value=100000.0, 
        value=3000.0,
        step=1.0
    )
    time_2 = st.number_input(
        "Time for Trial 2 (seconds)", 
        min_value=1.0, 
        max_value=100000.0, 
        value=720.0,
        step=1.0
    )
    power_2 = st.number_input(
        "Average Power for Trial 2 (Watts)",
        min_value=0.0,
        max_value=2000.0,
        value=250.0,
        step=1.0
    )
    
    if st.button("Calculate Critical Power"):
        if time_1 == time_2:
            st.error("Trial times must be different.")
        elif power_1 == power_2:
            st.error("Trial powers must be different.")
        else:
            cp = calculate_critical_power(power_1, time_1, power_2, time_2)
            if cp is None:
                st.error("Invalid input for calculation.")
            else:
                st.subheader("Result")
                st.metric("Critical Power (W)", f"{cp:.2f} W")
                st.write(f"This is your estimated critical power based on the two trials.")

                # Power zones as % of CP
                zone_boundaries = [0.7, 0.8, 0.9, 1.0, 1.2]
                zone_labels = [
                    "Z1 (<70% CP)",
                    "Z2 (70-80% CP)",
                    "Z3 (80-90% CP)",
                    "Z4 (90-100% CP)",
                    "Z5 (100-120% CP)",
                    "Z6 (>120% CP)"
                ]
                zone_ranges = [
                    f"< {cp * zone_boundaries[0]:.0f} W",
                    f"{cp * zone_boundaries[0]:.0f} - {cp * zone_boundaries[1]:.0f} W",
                    f"{cp * zone_boundaries[1]:.0f} - {cp * zone_boundaries[2]:.0f} W",
                    f"{cp * zone_boundaries[2]:.0f} - {cp * zone_boundaries[3]:.0f} W",
                    f"{cp * zone_boundaries[3]:.0f} - {cp * zone_boundaries[4]:.0f} W",
                    f"> {cp * zone_boundaries[4]:.0f} W"
                ]
                zones = [
                    {"Zone": zone_labels[i], "Power Range": zone_ranges[i]} for i in range(6)
                ]
                st.subheader("Training Zones (by % of Critical Power)")
                st.table(zones)

if __name__ == "__main__":
    main()