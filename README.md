# 🧲 LHC Magnet Cryogenic Control Simulation (PID)

![Status](https://img.shields.io/badge/Simulation-Active-success?style=for-the-badge)
![Domain](https://img.shields.io/badge/Domain-Control_Theory_&_Thermodynamics-red?style=for-the-badge)
![Tech](https://img.shields.io/badge/Stack-Python_|_NumPy_|_Matplotlib-blue?style=for-the-badge)

## 🔭 Abstract
This project simulates the thermodynamic response of a **Superconducting Magnet** within the Large Hadron Collider (LHC). The objective was to design a robust **Feedback Control Loop** capable of maintaining the critical operating temperature of **1.9 K** (Superfluid Helium range) while rejecting stochastic thermal disturbances caused by beam losses.

The simulation implements a discrete-time **PID (Proportional-Integral-Derivative) Controller** from first principles, demonstrating the stability requirements for high-energy physics instrumentation.

---

## 🧮 Mathematical Framework

### 1. System Dynamics (The Plant)
The magnet's temperature $T(t)$ is modeled as a first-order thermodynamic system. The rate of temperature change is defined by the balance between the cooling power (cryogenics) and external heat loads (beam loss + ambient leaks):

$$\frac{dT}{dt} = -\alpha (T(t) - T_{cool}) + \beta \cdot P_{disturbance}(t)$$

Where:
* $\alpha$: Thermal inertia coefficient (related to the specific heat capacity of the Niobium-Titanium coil).
* $T_{cool}$: The temperature of the coolant (Superfluid Helium).
* $P_{disturbance}$: Stochastic heat injection from beam losses.

### 2. The Control Law (PID Algorithm)
To maintain the target Setpoint ($SP = 1.9K$), the controller calculates the error $e(t) = T(t) - SP$. The control signal $u(t)$ (valve opening %) is computed as:

$$u(t) = K_p e(t) + K_i \int_{0}^{t} e(\tau) d\tau + K_d \frac{de(t)}{dt}$$

* **Proportional ($K_p$):** Provides immediate reaction to thermal deviation.
* **Integral ($K_i$):** Eliminates steady-state error (offset) to ensure $T \to 1.9K$ precisely.
* **Derivative ($K_d$):** Dampens overshoot and ringing during rapid disturbance rejection.

---

## 💻 Implementation Details
The simulation was built in pure Python to demonstrate algorithmic understanding without reliance on "black-box" control libraries.

| Parameter | Value | Justification |
| :--- | :--- | :--- |
| **Sampling Rate** | 100 Hz | High-frequency polling for real-time stability. |
| **$K_p$ Gain** | 8.0 | Aggressive response to keep temp low. |
| **$K_i$ Gain** | 0.2 | Slow integration to remove residual offset. |
| **$K_d$ Gain** | 2.5 | Heavy dampening to prevent oscillation. |

### Stochastic Disturbance Model
A "Beam Loss Event" is injected at $t=100s$, introducing a sudden thermal spike of **50W**. The controller must reject this disturbance within $<30$ seconds to prevent a magnet quench.

---

## 📉 Simulation Results
The graph below visualizes the system response.
* **Phase 1 (0-75s):** Rapid cooling from ambient (300K) to operating temp (1.9K).
* **Phase 2 (100-130s):** The red zone represents a high-energy **Beam Loss Event**.
* **Conclusion:** The PID controller successfully counteracts the heat spike, returning the system to stability with minimal oscillation.

![PID Control Graph](pid_control_report.png)

---

## 🛠️ Usage
```bash
# Clone the repository
git clone https://github.com/PradyumnShirsath/lhc-cryo-sim.git

# Run the simulation
python cryo_controller.py

---
*Author: Pradyumn Shirsath | Researching Control Theory & High-Energy Physics Instrumentation*