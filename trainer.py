from core.model import TeaDeer


td = TeaDeer()
td.markDrafts('traning/preparing/','traning/draft/')
# td.load('models/640_normal.pt')
#
#
#
# results =  td.detect('media',stream=True)
# for r in results:
#     td.plot(r)