def test_database_create_and_insert(tmp_path):
    from models import Database
    dbfile = tmp_path / "test.db"
    conn = f"sqlite:///{dbfile}"
    db = Database(conn)
    # insert a team
    teams = [{'external_id': 9999, 'name': 'Test FC', 'shortName': 'TFC', 'tla': 'TFC', 'venue': 'Test Stadium'}]
    db.upsert_teams(teams)
    rows = db.get_teams()
    assert any(r['external_id'] == 9999 for r in rows)
