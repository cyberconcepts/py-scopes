# tests/tlib_storage.py

"""Test implementation for the `scopes.storage` package."""

from datetime import datetime
from scopes.storage import concept, folder, message, topic, tracking


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

    n = tracks.remove(tr03)
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
    ch1.set('name', 'level2-item1')
    ch1.storeTrack()

    storage.commit()


def test_type(self, config):
    storage = config.storageFactory(config.dbschema)
    storage.dropTable('types')
    concept.setupCoreTypes(storage)
    types = storage.getContainer(concept.Type)
    tps = list(types.query())
    self.assertEqual(len(tps), 7)

    tfolder = types.queryLast(name='folder')
    fldrs = list(tfolder.values())
    self.assertEqual(len(fldrs), 2)
    self.assertEqual(fldrs[0].name, 'top')

    storage.commit()


def test_topic(self, config):
    storage = config.storageFactory(config.dbschema)
    storage.dropTable('rels')
    rels = storage.getContainer(concept.Triple)
    storage.dropTable('topics')
    topics = storage.getContainer(topic.Topic)
    types = storage.getContainer(concept.Type)
    concept.storePredicate(storage, concept.defaultPredicate)
    root = folder.Root(storage)
    root['top']['topics'] = ftopics = folder.Folder()
    ttopic = types.queryLast(name='topic')
    self.assertEqual(ttopic.name, 'topic')
    ftopics.setTarget(ttopic)
    self.assertEqual(ftopics.getTarget().name, 'topic')

    tp_itc = topic.Topic('itc', data=dict(
        title='ITC', description='Information and Communication Technology'))
    topics.save(tp_itc)
    tp_proglang = topic.Topic('prog_lang', data=dict(
        title='Programming Languages', 
        description='Programming Languages'))
    topics.save(tp_proglang)
    #storage.commit() # avoid "database locked" error with sqlite
    tp_itc.addChild(tp_proglang)

    c = list(tp_itc.children())
    self.assertEqual(c[0].name, 'prog_lang')

    storage.commit()


def test_message(self, config):
    storage = config.storageFactory(config.dbschema)
    storage.dropTable('messages')
    messages = storage.create(message.Messages)
    m01 = message.Message('system', 'data', 'session', 'V1_317784226621611853')
    m01.update(dict(userid='tst9'))
    mid01 = messages.save(m01)

    storage.commit()


