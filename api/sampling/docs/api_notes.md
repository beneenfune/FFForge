pymatgen.core.structure:
Immutable class representation of a molecule containing information about atomic species, coordinates, charge, spin multiplicity, binary indicators of whether to check for sites <1Å apart and whether charge and spin multiplicities are compatible, properties and labels of each site, and a dictionary of properties.

sklearn.decomposition.PCA:
Class used to perform singular value decomposition.
pca.components - principle axes sorted by decreasing explained_variance
pca.singular_values_ - singular values for each component
pca.mean_; pca.n_components_; pca.n_samples_; pca.explained_variance
pca.fit(X) - fit the model to X

sklearn.cluster.Birch:
Class implementation of BIRCH clustering algorithm. Contains threshold distance to merge clusters, maximum number of subclusters per node, number of final clusters, and indicators of whether to compute labels and overwrite data.
birch.fit(X) - build a tree
birch.predict(X) - returns array of centroids of clusters