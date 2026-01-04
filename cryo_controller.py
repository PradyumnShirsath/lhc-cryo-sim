import numpy as np
import matplotlib.pyplot as plt

# --- 1. The Physics Model (The "Plant") ---
class LHCMagnet:
    def __init__(self):
        self.temperature = 300.0  # Start at room temp (Kelvin)
        self.target_temp = 1.9    # Target: Superfluid Helium temp
        self.cooling_power = 0.0
        
    def update(self, control_signal, disturbance_heat):
        """
        Simulates one time-step of the magnet's thermodynamics.
        control_signal: 0 to 100% (How much cooling valve is open)
        disturbance_heat: External heat from beam losses
        """
        # Physics: Cooling lowers temp, Disturbance raises it
        # Inertia factor (0.98) makes it react slowly like real metal
        cooling_effect = (control_signal * 0.1) 
        warming_effect = disturbance_heat * 0.05
        
        # Thermodynamics equation
        self.temperature = (self.temperature * 0.98) - cooling_effect + warming_effect
        
        # Physics constraints (Temp can't go below absolute zero)
        if self.temperature < 0: self.temperature = 0

# --- 2. The Control Logic (The "Brain") ---
class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp  # Proportional (Speed)
        self.Ki = Ki  # Integral (Precision)
        self.Kd = Kd  # Derivative (Stability)
        self.prev_error = 0
        self.integral = 0
        
    def compute(self, target, current):
        error = current - target
        
        # P-Term: React to current error
        P = self.Kp * error
        
        # I-Term: Fix accumulated long-term error
        self.integral += error
        I = self.Ki * self.integral
        
        # D-Term: React to speed of change (dampening)
        derivative = error - self.prev_error
        D = self.Kd * derivative
        
        self.prev_error = error
        
        # Output: 0-100% valve opening
        output = P + I + D
        return max(0, min(100, output)) # Clamp between 0% and 100%

# --- 3. The Simulation Loop ---
def run_simulation():
    # Setup
    magnet = LHCMagnet()
    # Tuning values: Kp=5.0 (Strong reaction), Ki=0.1 (Fix offset), Kd=0.5 (Dampen oscillation)
    pid = PIDController(Kp=8.0, Ki=0.2, Kd=2.5) 
    
    history = {'time': [], 'temp': [], 'setpoint': []}
    
    print("🚀 Starting LHC Cryogenic Cooling Sequence...")
    
    for t in range(200):
        # A. Define the Setpoint (We want 1.9 K)
        setpoint = 1.9
        
        # B. Create a Disturbance (Beam Loss Event at t=100)
        disturbance = 2.0 if t > 100 and t < 120 else 295.0 # Ambient heat initially
        if t > 50: disturbance = 0.0 # Vacuum insulation kicks in
        if t > 100 and t < 130: disturbance = 50.0 # HEAT SPIKE!
        
        # C. Compute Control Signal (PID)
        control_action = pid.compute(setpoint, magnet.temperature)
        
        # D. Apply to Physics Model
        magnet.update(control_action, disturbance)
        
        # E. Record Data
        history['time'].append(t)
        history['temp'].append(magnet.temperature)
        history['setpoint'].append(setpoint)

    return history

# --- 4. Visualization (The Evidence) ---
def plot_results(data):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot Target Line
    ax.plot(data['time'], data['setpoint'], color='#00FF00', linestyle='--', label='Target (1.9 K)')
    
    # Plot Actual Temperature
    ax.plot(data['time'], data['temp'], color='#00D4FF', linewidth=2, label='Magnet Temp')
    
    # Highlight the "Crisis" Zone
    ax.axvspan(100, 130, color='red', alpha=0.3, label='Beam Loss Event (Disturbance)')
    
    ax.set_title("LHC Magnet Cryogenic Control Simulation (PID)", fontsize=14, fontweight='bold', color='white')
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (Kelvin)")
    ax.legend()
    ax.grid(True, alpha=0.2)
    
    print("✅ Simulation Complete. Generating Graph...")
    plt.savefig('pid_control_report.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    data = run_simulation()
    plot_results(data)