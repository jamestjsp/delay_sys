# delay_sys

A Python library for discretizing continuous-time transfer functions with time delays.

## Overview

`delay_sys` provides utilities for converting continuous-time control systems to discrete-time while incorporating deadtime delays. The library features a `DelayTransferFunction` class that extends `python-control`'s TransferFunction to natively handle time delays.

## Installation

### Using pip
```bash
pip install delay_sys
```

### Using uv (recommended for development)
```bash
git clone https://github.com/jamestjsp/delay_sys.git
cd delay_sys
uv sync
```

For development installation with pip:
```bash
git clone https://github.com/jamestjsp/delay_sys.git
cd delay_sys
pip install -e .
```

## Command-line Interface

The package includes a demonstration command that shows step response comparison:

```bash
# Run the demonstration
uv run delay_sys
```

This will:
- Create a first-order continuous system G(s) = 1/(5s + 1)
- Discretize it with sampling time h = 0.5 minutes
- Add a deadtime of 2.0 minutes
- Display both systems and plot their step and frequency responses

## Quick Start

### Using DelayTransferFunction directly
```python
import control as ct
import delay_sys

# Create a continuous-time transfer function and discretize
G = ct.tf([1], [1, 2, 1])  # 1/(s^2 + 2s + 1)
G_discrete = ct.sample_system(G, 0.1, method='zoh')

# Create with deadtime
Gd = delay_sys.DelayTransferFunction(
    num=G_discrete.num[0][0],
    den=G_discrete.den[0][0],
    dt=0.1,
    deadtime=0.3
)

print(Gd)
```

### Using helper functions
```python
from delay_sys.delayed_tf import create_fopdt

# Create FOPDT system directly
Gd = create_fopdt(
    gain=2.0,
    time_constant=1.5, 
    dt=0.1,
    deadtime=0.3
)

print(Gd)  # Shows transfer function with deadtime info
```

## API Reference

### `DelayTransferFunction`

A transfer function class with explicit time delay support.

**Parameters:**
- `num` (list of float): Numerator coefficients of the base transfer function
- `den` (list of float): Denominator coefficients of the base transfer function  
- `dt` (float): The sampling period for the discrete-time system. Must be > 0
- `deadtime` (float, optional): The deadtime in the same units as `dt`. Defaults to 0.0

**Attributes:**
- `deadtime` (float): The deadtime value used in the system

## Examples

### Basic Discretization
```python
import control as ct
import delay_sys

# First-order system
G = ct.tf([2], [1, 3])
G_discrete = ct.sample_system(G, 0.1, method='zoh')
Gd = delay_sys.DelayTransferFunction(
    G_discrete.num[0][0], 
    G_discrete.den[0][0], 
    dt=0.1
)
print(f"Deadtime: {Gd.deadtime}")  # Access deadtime attribute
```

### With Deadtime
```python
# Add 0.5 second deadtime
Gd_delayed = delay_sys.DelayTransferFunction(
    G_discrete.num[0][0], 
    G_discrete.den[0][0], 
    dt=0.1, 
    deadtime=0.5
)
print(Gd_delayed)  # Shows transfer function with deadtime info
```

### Different Discretization Methods
```python
# Using Tustin (bilinear) method
G_tustin = ct.sample_system(G, 0.1, method='tustin')
Gd_tustin = delay_sys.DelayTransferFunction(
    G_tustin.num[0][0], 
    G_tustin.den[0][0], 
    dt=0.1
)
```

### Direct DelayTransferFunction Usage
```python
# Create a first-order system with deadtime
fopdt_system = delay_sys.DelayTransferFunction(
    num=[0.095],             # Numerator coefficients
    den=[1, -0.819],         # Denominator coefficients
    dt=0.1,                  # 100ms sampling
    deadtime=0.25            # 250ms deadtime
)

# Use with python-control functions
t, y = ct.step_response(fopdt_system)
```

### System Analysis
```python
import numpy as np
import matplotlib.pyplot as plt
from delay_sys.delayed_tf import create_fopdt

# Create system with deadtime using helper
Gd = create_fopdt(gain=1.0, time_constant=1.0, dt=0.1, deadtime=0.3)

# Analyze stability margins
gm, pm, wg, wp = ct.margin(Gd)
print(f"Gain margin: {gm:.2f}, Phase margin: {pm:.2f}°")

# Plot frequency response
w = np.logspace(-2, 2, 100)
ct.bode(Gd, w)
plt.show()
```

## Features

- **Native deadtime support**: `DelayTransferFunction` class with explicit deadtime handling
- **Multiple discretization methods**: Supports all methods available in `python-control`
- **Integer delay implementation**: Automatically rounds deadtime to nearest integer number of samples
- **Full compatibility**: Works seamlessly with `python-control` functions
- **Input validation**: Comprehensive error checking for invalid parameters
- **SISO systems**: Currently supports Single-Input Single-Output systems

## Requirements

- Python >= 3.8
- control >= 0.9.0
- numpy >= 1.19.0
- matplotlib >= 3.0.0

## Development

### Using uv (recommended)
```bash
# Clone and setup
git clone https://github.com/jamestjsp/delay_sys.git
cd delay_sys

# Install dependencies and run
uv run delay_sys

# Run tests
uv run pytest

# Create FOPDT system example
uv run python -c "from delay_sys.delayed_tf import create_fopdt; sys = create_fopdt(gain=2.0, time_constant=1.0, dt=0.1, deadtime=0.3); print(sys)"
```

### Traditional development setup
```bash
pip install -e .
python -m delay_sys
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
