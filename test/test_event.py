import xindmap.event


def test_basic_event():
    class Source(xindmap.event.EventSource):
        def __init__(self):
            super().__init__(("a", "b"))

    source = Source()

    event_a_dispatched = [False]
    event_b_dispatched = [False]

    def toggle_a():
        event_a_dispatched[0] = not event_a_dispatched[0]

        source._dispatch_event(xindmap.event.Event("b"))

        assert not event_b_dispatched[0]

    def toggle_b():
        event_b_dispatched[0] = not event_a_dispatched[0]

    source.register_callbacks("a", lambda event_source, event: toggle_a())
    source.register_callbacks("b", lambda event_source, event: toggle_b())

    source._dispatch_event(xindmap.event.Event("a"))

    assert event_a_dispatched and event_b_dispatched
