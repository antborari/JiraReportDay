import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import jira_report

class TestJiraReport(unittest.TestCase):

    @patch('jira_report.JIRA')
    def test_get_jira_client(self, MockJIRA):
        # Setup env vars mock
        with patch.dict('os.environ', {
            'JIRA_URL': 'http://test.com', 
            'JIRA_EMAIL': 'user@test.com', 
            'JIRA_API_TOKEN': 'token'
        }):
            client = jira_report.get_jira_client()
            self.assertIsNotNone(client)
            MockJIRA.assert_called_with(server='http://test.com', basic_auth=('user@test.com', 'token'))

    def test_get_worklogs_last_30_days(self):
        # Mock JIRA client
        mock_jira = MagicMock()
        
        # Configurar usuario actual
        mock_myself = {'accountId': 'user123', 'name': 'test_user', 'emailAddress': 'user@test.com'}
        mock_jira.myself.return_value = mock_myself
        
        # Configurar Issues
        mock_issue1 = MagicMock()
        mock_issue1.id = '10001'
        mock_issue2 = MagicMock()
        mock_issue2.id = '10002'
        
        mock_jira.search_issues.return_value = [mock_issue1, mock_issue2]
        
        # Configurar Worklogs
        # Worklog 1: Hace 2 días, usuario correcto (3600 segundos = 1 hora)
        date_2_days_ago = datetime.now() - timedelta(days=2)
        wl1 = MagicMock()
        wl1.author.accountId = 'user123'
        wl1.started = date_2_days_ago.strftime('%Y-%m-%dT10:00:00.000+0000')
        wl1.timeSpentSeconds = 3600
        
        # Worklog 2: Hace 2 días, usuario correcto, otra hora (3600 segundos = 1 hora)
        wl2 = MagicMock()
        wl2.author.accountId = 'user123'
        wl2.started = date_2_days_ago.strftime('%Y-%m-%dT14:00:00.000+0000')
        wl2.timeSpentSeconds = 3600
        
        # Worklog 3: Hace 40 días (fuera de rango)
        date_40_days_ago = datetime.now() - timedelta(days=40)
        wl3 = MagicMock()
        wl3.author.accountId = 'user123'
        wl3.started = date_40_days_ago.strftime('%Y-%m-%dT10:00:00.000+0000')
        wl3.timeSpentSeconds = 3600
        
        # Worklog 4: Usuario incorrecto
        wl4 = MagicMock()
        wl4.author.accountId = 'other_user'
        wl4.started = date_2_days_ago.strftime('%Y-%m-%dT10:00:00.000+0000')
        wl4.timeSpentSeconds = 3600

        # Asignar worklogs a issues (issue1 tiene wl1 y wl3, issue2 tiene wl2 y wl4)
        def get_worklogs_side_effect(issue_id):
            if issue_id == '10001':
                return [wl1, wl3]
            elif issue_id == '10002':
                return [wl2, wl4]
            return []
            
        mock_jira.worklogs.side_effect = get_worklogs_side_effect
        
        # Ejecutar
        daily_hours = jira_report.get_worklogs_last_30_days(mock_jira)
        
        # Verificar
        date_key = date_2_days_ago.strftime('%Y-%m-%d')
        self.assertIn(date_key, daily_hours)
        self.assertAlmostEqual(daily_hours[date_key], 2.0) # 1h + 1h
        
        date_40_key = date_40_days_ago.strftime('%Y-%m-%d')
        self.assertNotIn(date_40_key, daily_hours)

if __name__ == '__main__':
    unittest.main()
