# import unittest
# from flask import template_rendered
# from contextlib import contextmanager
# from ..app import create_app
# import pytest

# @contextmanager
# def captured_templates(app):
#     """Context manager to capture templates being rendered"""
#     recorded = []
#     def record(sender, template, context, **extra):
#         recorded.append((template, context))
#     template_rendered.connect(record, app)
#     try:
#         yield recorded
#     finally:
#         template_rendered.disconnect(record, app)

# class TestHomeRoute(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app()
#         self.app.config['TESTING'] = True
#         self.client = self.app.test_client()
#         self.app_context = self.app.app_context()
#         self.app_context.push()

#     def tearDown(self):
#         self.app_context.pop()

#     def test_home_status_code(self):
#         """Test that the home page returns 200 status code"""
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)

#     def test_home_renders_template(self):
#         """Test that the home page renders the index.html template"""
#         with captured_templates(self.app) as templates:
#             response = self.client.get('/')
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(len(templates), 1)
#             template, context = templates[0]
#             self.assertEqual(template.name, 'index.html')

#     def test_home_returns_content(self):
#         """Test that the home page returns content"""
#         response = self.client.get('/')
#         self.assertIn(b'<!DOCTYPE html>', response.data)

# if __name__ == '__main__':
#     unittest.main()