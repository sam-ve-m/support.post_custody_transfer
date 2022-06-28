from func.src.domain.snapshot.html.base.create_table import BaseTableDTO


dummy_table = "<table><b><th><td>"


def test_style_table():
    setattr(BaseTableDTO, "_table_color", None)
    styled_table = BaseTableDTO._style_table(dummy_table)
    assert '<div style="display: inline-block">' in styled_table
    assert '<table style="' in styled_table
    assert '<b style="' in styled_table
    assert '<th style="' in styled_table
    assert '<td style="' in styled_table
