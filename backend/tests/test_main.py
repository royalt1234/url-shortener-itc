def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_shorten_url(client):
    response = client.post("/shorten?original_url=https://example.com")
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert data["original_url"] == "https://example.com"
    return data["short_code"] # returning for use in another test conceptually

def test_shorten_url_custom_code(client):
    response = client.post("/shorten?original_url=https://example.com/custom&custom_code=mycustom")
    assert response.status_code == 200
    data = response.json()
    assert data["short_code"] == "mycustom"

def test_shorten_invalid_url(client):
    response = client.post("/shorten?original_url=not-a-url")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid URL"}

def test_shorten_duplicate_custom_code(client):
    client.post("/shorten?original_url=https://example.com/custom&custom_code=dup")
    response = client.post("/shorten?original_url=https://example.com/custom2&custom_code=dup")
    assert response.status_code == 400
    assert response.json() == {"detail": "Custom code already taken"}

def test_redirect_to_original(client):
    # Shorten first
    resp1 = client.post("/shorten?original_url=https://example.com/redirect&custom_code=redir")
    assert resp1.status_code == 200

    # Test redirect (Don't follow redirect so we can check the status code)
    resp2 = client.get("/redir", follow_redirects=False)
    assert resp2.status_code == 307
    assert resp2.headers["location"] == "https://example.com/redirect"

def test_redirect_not_found(client):
    response = client.get("/not-real-code")
    assert response.status_code == 404

def test_get_all_links(client):
    client.post("/shorten?original_url=https://example.com/link1&custom_code=l1")
    response = client.get("/api/links")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_analytics(client):
    # Create and click
    client.post("/shorten?original_url=https://example.com/stats&custom_code=stat")
    client.get("/stat", follow_redirects=False)

    # Check analytics
    response = client.get("/api/analytics/stat")
    assert response.status_code == 200
    data = response.json()
    assert data["total_clicks"] == 1
    assert len(data["click_details"]) == 1

def test_delete_link(client):
    client.post("/shorten?original_url=https://example.com/del&custom_code=del_me")
    
    # Check it exists
    assert client.get("/api/analytics/del_me").status_code == 200
    
    # Delete it
    del_resp = client.delete("/api/links/del_me")
    assert del_resp.status_code == 200
    
    # Check it's gone
    assert client.get("/api/analytics/del_me").status_code == 404

def test_get_stats(client):
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_links" in data
    assert "total_clicks" in data
