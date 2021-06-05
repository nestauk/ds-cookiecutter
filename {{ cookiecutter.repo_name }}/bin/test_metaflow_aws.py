import metaflow as mf

mf.namespace(None)

m = mf.Metaflow()

assert m.metadata == mf.plugins.metadata.service.ServiceMetadataProvider, m.metadata
assert len(m.flows) > 0, m.flows
