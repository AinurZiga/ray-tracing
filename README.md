# ray-tracing
Ray-tracing deterministic model

### Requirements
- Python 3.10.5
- PySide2 5.15.5
- NumPy 1.22.4
- Numba 0.55.2

### Supported features
1. Image method for finding reflected rays
2. Single and double bounce reflection. Each new bounce significantly increases computation time as the image method finds reflected rays recursively.
3. Coefficients of reflection and passage are found based on Recommendation ITU-R P. 2040-1.
4. Indoor scenario, but the map is only supported in its own format. One instance in the /maps folder is used in examples.
5. MIMO system with finding channel matrix and computation of quality metrics such as capacity, rank, and condition number.
6. Coverage map with found quality metrics.

Code snippets are available in the folder /examples.

