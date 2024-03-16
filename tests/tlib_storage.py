# tests/tlib_storage.py

"""Test implementation for the `scopes.storage` package."""

from datetime import datetime
from scopes.storage import concept, folder, topic, tracking


def test_tracking(self, config):
    storage = config.storageFactory(config.dbschema)
    storage.dropTable('tracks')
    tracks = storage.create(tracking.Container)

    tr01 = tracking.Track('t01', 'john')
    tr01.update(dict(activity='testing'))
    self.assertEqual(tr01.head, {'taskId': 't01', 'userName': 'john'})
    self.assertEqual(tr01.taskId, 't01')
    self.assertEqual(tr01.userName, 'john')

    self.assertTrue(tracks.getTable() is not None)

    trid01 = tracks.save(tr01)
    self.assertTrue(trid01 > 0)

    #tr01a = tracks.get(trid01)
    tr01a = tracks['%07i' % trid01]
    self.assertEqual(tr01a.head, tr01.head)
    self.assertEqual(tr01a.trackId, trid01)
    self.assertEqual(tr01a.data.get('activity'), 'testing')

    tr01a.update(dict(text='Set up unit tests.'))
    tr01a.timeStamp = None
    self.assertTrue(tracks.save(tr01a) > 0)

    tr01b = tracks.queryLast(taskId='t01')
    self.assertEqual(tr01b.head, tr01.head)
    self.assertNotEqual(tr01b.trackId, trid01)
    self.assertEqual(tr01b.data.get('activity'), 'testing')

    tr02 = tracking.Track('t02', 'jim', trackId=31, timeStamp=datetime(2023, 11, 30),
                        data=dict(activity='concept'))
    trid02 = tracks.upsert(tr02)
    self.assertEqual(trid02, 31)
    self.assertEqual(tr02.uid, 'rec-31')
    tr02.trackId = trid01
    trid021 = tracks.upsert(tr02)
    self.assertEqual(trid021, trid01)
    self.assertEqual(tr02.uid, 'rec-' + str(trid01))

    tr03 = storage.getItem('rec-31')
    self.assertEqual(tr03.trackId, 31)

    n = tracks.remove(31)
    self.assertEqual(n, 1)
    self.assertEqual(tracks.get(31), None)

    storage.commit()


def test_folder(self, config):
    storage = config.storageFactory(config.dbschema)
    storage.dropTable('folders')
    root = folder.Root(storage)
    self.assertEqual(list(root.keys()), [])
    root['top'] = folder.Folder()
    self.assertEqual(list(root.keys()), ['top'])
    top = root['top']
    top['child1'] = folder.Folder(data=dict(title='First Child'))
    self.assertEqual(list(top.keys()), ['child1'])
    ch1 = top['child1']
    self.assertEqual(ch1.parent, top.rid)
    self.assertEqual(list(top.keys()), ['child1'])

    storage.commit()


def test_type(self, config):
    storage = config.storageFactory(config.dbschema)
    storage.dropTable('types')
    concept.setupCoreTypes(storage)

    types = storage.getContainer(concept.Type)
    tps = list(types.query())
    self.assertEqual(len(tps), 6)
    self.assertEqual(tps[0].name, 'track')

    tfolder = types.queryLast(name='folder')
    fldrs = list(tfolder.values())
    self.assertEqual(len(fldrs), 2)
    self.assertEqual(fldrs[0].name, 'top')

    storage.commit()


def test_topic(self, config):
    storage = config.storageFactory(config.dbschema)
    storage.dropTable('topics')
    topics = storage.getContainer(topic.Topic)
    types = storage.getContainer(concept.Type)
    concept.storePredicate(storage, concept.defaultPredicate)
    root = folder.Root(storage)
    root['top']['topics'] = ftopics = folder.Folder()
    ttopic = types.queryLast(name='topic')
    self.assertEqual(ttopic.name, 'topic')
    ftopics.setTarget(ttopic)
    self.assertEqual(ftopics.ref, 'type-6')

    tp_itc = topic.Topic('itc', data=dict(
        title='ITC', description='Information and Communication Technology'))
    topics.save(tp_itc)

    storage.commit()
    
