# Ray-tracing
Ray-tracing deterministic model


### Supported features
1. Image method for finding reflected rays
2. Single and double bounce reflection. Each new bounce significantly increases computation time as the image method finds reflected rays recursively.
3. Coefficients of reflection and passage are found based on Recommendation ITU-R P. 2040-1.
4. Indoor scenario, but the map is only supported in its own format. One instance in the /maps folder is used in examples.
5. MIMO system with finding channel matrix and computation of quality metrics such as capacity, rank, and condition number.
6. Coverage map with found quality metrics.

Code snippets are available in the folder /examples.


### Not supported (in development)
1. OpenStreetMap for the outdoor scenarios.
2. Diffuse scattering.
3. Diffraction.
4. Different types of polarization. Only vertical polarisation is available so far.
