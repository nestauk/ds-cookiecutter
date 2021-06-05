import metaflow as mf

m = mf.Metaflow()
print(m.metadata)
print(mf.get_metadata())
assert m.metadata == mf.plugins.metadata.service.ServiceMetadataProvider
print(m.flows)
print(mf.Flow("HelloAWSFlow"))
assert len(m.flows) > 0
