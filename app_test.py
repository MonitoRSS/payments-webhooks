from app import app as flaskapp
from pytest import fixture, MonkeyPatch


@fixture
def client():
    flaskapp.config['TESTING'] = True
    return flaskapp.test_client()


@fixture
def monkeypatch():
    return MonkeyPatch()


def test_health(client):
    res = client.get('/api/health')
    assert res.get_json() == {"ok": 1}


def test_processing_error(client):
    """
    If something went wrong while processing the payload, return a success 0
    In reality, it doesn't matter since it's still returning a 200 status to Stripe, but
    this is just for testing purposes
    """
    res = client.post('/api/webhook', json={
        "type": "ooglaboo"
    })
    assert res.get_json() == {"success": 0}


def test_unhandled_event(client, monkeypatch):
    """
    An unhandled event should always return a success response
    """
    def validate_webhook_payload(request):
        return {
            "type": "ooglaboo"
        }
    mp = MonkeyPatch()
    mp.setattr('utils.validate_webhook_payload.validate_webhook_payload',
               validate_webhook_payload)
    res = client.post('/api/webhook', json={
        "type": "ooglaboo"
    })
    assert res.get_json() == {"success": 1}
