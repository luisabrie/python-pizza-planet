import pytest

from app.controllers.report import ReportController

def test_get_report_empty(app):
    
    report, err = ReportController.get_reports()
    pytest.assume(err is None)
    pytest.assume(report.get('most_requested_ingredient') == {
        'name': '',
        'total': 0
    })
    pytest.assume(report.get('month_with_most_revenue') == {
        'month': '',
        'total': 0
    })
    pytest.assume(report.get('top_three_customers') == [])

def test_get_report_most_requested_ingredient(app,create_report_order_mock):
    report, err = ReportController.get_reports()
    pytest.assume(err is None)
    pytest.assume(report.get('most_requested_ingredient') == {
        'name': 'ingredient 2',
        'total': 5
    })

def test_get_report_month_with_most_revenue(app,create_report_order_mock):
    report, err = ReportController.get_reports()
    pytest.assume(err is None)
    pytest.assume(report.get('month_with_most_revenue') == {
        'month': 'May',
        'total': 27
    })

def test_get_report_top_three_customers(app,create_report_order_mock):
    report, err = ReportController.get_reports()
    print(report)
    pytest.assume(err is None)
    pytest.assume(report.get('top_three_customers') == [
        {
            'name': 'client 2',
            'total': 3
        },
        {
            'name': 'client 3',
            'total': 2
        },
        {
            'name': 'client 4',
            'total': 1
        }
    ])