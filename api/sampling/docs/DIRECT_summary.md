A brief summary of DIRECT (DImensionality-Reduced Encoded Clusters with sTratified) sampling methodology from “Robust training of machine learning interatomic potentials with dimensionality reduction and stratified sampling,” Qi et al., 2024.

Step 0: Configuration space generation. As in any sampling method this is essentially the initial, “raw” sample from which the final DIRECT sample will be drawn. In this case, a set of observed structures.

Step 1: Featurization & encoding. Designing the features of observation and defining each datapoint as a representative vector based on those features. In the case of the article, they used 128-element vectors based on the M3GNet model of formation energies.

Step 2: Dimensionality reduction. Perform a PCA on the normalized vectors from step 1. The authors use Kaiser’s rule to redefine the feature space as components with eigenvalues >1, i.e. those which explain the greatest variance.

Step 3: Clustering. Group similar structures together based on particular characteristics using the “Balanced Iterative Reducing and Clustering using Hierarchies” algorithm, assigning structures to groups based on their proximity in the dimensionality-reduced space from step 2. The number of groups n is chosen to maximize accuracy and/or computational efficiency, as the number of clusters will determine the size of the final stratified sample.

Step 4: Stratified sampling. Sample the k most representative structures of each cluster, i.e. those with vectors closest to the centroid of the cluster. For clusters of size less than k, users can decide to allow duplicate sampling or not. The number of vectors sampled k is, like n, determined by desired accuracy and available computing power.