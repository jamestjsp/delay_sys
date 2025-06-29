import control as ct
import numpy as np
from .delayed_tf import DelayTransferFunction

__all__ = ['DelayTransferFunction']


def main():
    """Command-line interface for delay_sys demonstration."""
    import matplotlib.pyplot as plt
    from .delayed_tf import create_fopdt

    print("delay_sys - Discrete System with Delay Demonstration")
    print("=" * 50)

    # Define the continuous-time plant model G(s) = 1 / (5s + 1)
    s_num = [1]
    s_den = [5, 1]
    Gs = ct.tf(s_num, s_den)

    # Define the desired sampling and deadtime parameters
    h = 0.5      # sampling period in minutes
    deadtime = 2.0 # deadtime in minutes

    # Discretize manually and create DelayTransferFunction
    base_discrete = ct.sample_system(Gs, h, method='zoh')
    Gz_delayed = DelayTransferFunction(
        base_discrete.num[0][0], 
        base_discrete.den[0][0], 
        h, 
        deadtime
    )

    # Example of creating DelayTransferFunction using helper function
    direct_delayed = create_fopdt(
        gain=1.0, time_constant=5.0, dt=h, deadtime=deadtime
    )

    print("Original Continuous System:")
    print(Gs)
    print(f"\nDiscretized and Delayed System (manual approach):")
    print(Gz_delayed)
    print(f"\nDirect DelayTransferFunction (using create_fopdt):")
    print(direct_delayed)

    # --- Plot the step response ---
    t_final = 20
    t = np.arange(0, t_final, h)
    t_fine = np.linspace(0, t_final, 500)

    # Get the response of the final discrete system
    t_d, y_d = ct.step_response(Gz_delayed, T=t)

    # Get the response of an ideal continuous system with delay
    t_c, y_c = ct.step_response(Gs, T=t_fine)

    plt.figure(figsize=(12, 8))
    
    # Plot step responses
    plt.subplot(2, 1, 1)
    plt.plot(t_c + deadtime, y_c, 'g--', label='Ideal Delayed Continuous Response')
    plt.plot(t_d, y_d, 'bo-', drawstyle='steps-post', label='DelayTransferFunction Response')
    plt.title('Step Response Comparison')
    plt.xlabel('Time (min)')
    plt.ylabel('Output')
    plt.grid(True)
    plt.legend()
    
    # Plot frequency response
    plt.subplot(2, 1, 2)
    w = np.logspace(-2, 1, 100)
    mag, phase, omega = ct.bode(Gz_delayed, w, plot=False)
    plt.semilogx(omega, 20 * np.log10(mag), 'b-', label='Magnitude (dB)')
    plt.xlabel('Frequency (rad/s)')
    plt.ylabel('Magnitude (dB)')
    plt.title('Frequency Response')
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()