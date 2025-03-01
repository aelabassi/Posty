from app import schema
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    for post in res.json():
        new_post = schema.Post(**post["post"])
        assert new_post.id == post["post"]["id"]
        assert new_post.title == post["post"]["title"]
        assert new_post.content == post["post"]["content"]
    assert res.status_code == 200

def test_get_post_by_id(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schema.Post(**res.json()["post"])
    assert post.id == test_posts[0].id
    assert post.title == test_posts[0].title
    assert post.content == test_posts[0].content

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/6000")
    assert res.status_code == 404

@pytest.mark.parametrize("title, content, published", [
    ("Batman dark patterns", "During the past rocky days of Batman with Alfred", True),
    ("Batman issue 158", "Whoo, Batman old foe--Hush is back in town!!", True),
    ("New Design for Batman", "Father is getting a new costume and logo.", False)
])
def test_create_post(authorized_client, test_posts, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schema.Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]

def test_delete_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title":"I'm getting my own costume",
        "content":"See me in the new <still thinking about the code name> run",
        "id":test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    update_post = schema.Post(**res.json())
    assert res.status_code == 200
    assert update_post.title == data["title"]
    assert update_post.content == data["content"]

def test_update_other_user_post(authorized_client, test_posts, test_user, test_other_user):
    data = {
        "title": "I'm getting my own costume",
        "content": "See me in the new <still thinking about the code name> run",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_update_non_existing_post(authorized_client, test_posts, test_user):
    data = {
        "title": "I'm getting my own costume",
        "content": "See me in the new <still thinking about the code name> run",
        "id": test_posts[3].id
    }
    res = authorized_client.put("/posts/6000", json=data)
    assert res.status_code == 404

def test_delete_non_existing_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete("/posts/6000")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_unauthorized_user_create_post(client, test_posts, test_user):
    res = client.post("/posts/", json={"title":"The $%&@ joker", "content":"He broke jim--jambo, I would kill him unlike my father"})
    assert res.status_code == 401

def test_unauthorized_user_update_post(client, test_posts, test_user):
    data = {
        "title": "I'm getting my own costume",
        "content": "See me in the new <still thinking about the code name> run",
        "id": test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
