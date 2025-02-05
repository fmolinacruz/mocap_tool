# src/visualization/motion_visualizer.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene,
                          QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from typing import Dict, List, Optional
import math

class MotionScene(QGraphicsScene):
   """Custom graphics scene for rendering motion data"""
   def __init__(self):
       super().__init__()
       self.skeleton_points = []
       self.motion_trail = []
       self.max_trail_length = 50
       
       # Set up visual styles
       self.skeleton_pen = QPen(QColor(0, 255, 0))  # Green for skeleton
       self.skeleton_pen.setWidth(2)
       self.trail_pen = QPen(QColor(0, 150, 255))   # Blue for motion trail
       self.trail_pen.setWidth(1)
       
   def update_skeleton(self, points: List[QPointF]):
       self.skeleton_points = points
       if points:
           self.motion_trail.append(points)
           if len(self.motion_trail) > self.max_trail_length:
               self.motion_trail.pop(0)
       self.update()
       
   def drawBackground(self, painter: QPainter, rect: QRectF):
       super().drawBackground(painter, rect)
       
       # Draw grid
       grid_pen = QPen(QColor(50, 50, 50))  # Dark grey
       grid_size = 50  # Grid cell size
       
       left = int(rect.left() - (rect.left() % grid_size))
       top = int(rect.top() - (rect.top() % grid_size))
       
       # Draw vertical lines
       for x in range(left, int(rect.right()), grid_size):
           painter.setPen(grid_pen)
           painter.drawLine(x, rect.top(), x, rect.bottom())
           
       # Draw horizontal lines
       for y in range(top, int(rect.bottom()), grid_size):
           painter.setPen(grid_pen)
           painter.drawLine(rect.left(), y, rect.right(), y)
           
   def drawForeground(self, painter: QPainter, rect: QRectF):
       super().drawForeground(painter, rect)
       
       # Draw motion trail
       for trail_points in self.motion_trail:
           painter.setPen(self.trail_pen)
           self._draw_skeleton(painter, trail_points, is_trail=True)
           
       # Draw current skeleton
       if self.skeleton_points:
           painter.setPen(self.skeleton_pen)
           self._draw_skeleton(painter, self.skeleton_points, is_trail=False)
           
   def _draw_skeleton(self, painter: QPainter, points: List[QPointF], is_trail: bool):
       if not points:
           return
           
       # Draw joints
       for point in points:
           if is_trail:
               painter.drawPoint(point)
           else:
               painter.drawEllipse(point, 3, 3)
               
       # Draw connections between joints
       if len(points) > 1:
           for i in range(len(points) - 1):
               painter.drawLine(points[i], points[i + 1])

class MotionVisualizer(QWidget):
   """Widget for visualizing motion capture data"""
   def __init__(self, parent=None):
       super().__init__(parent)
       
       layout = QVBoxLayout()
       
       self.info_label = QLabel("No data")
       layout.addWidget(self.info_label)
       
       # Create view and scene
       self.scene = MotionScene()
       self.view = QGraphicsView(self.scene)
       self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
       self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
       self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
       self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
       self.view.setBackgroundBrush(QBrush(QColor(30, 30, 30)))  # Dark background
       
       # Set up view transforms
       self.view.scale(1, -1)  # Flip Y axis to match 3D coordinate system
       layout.addWidget(self.view)
       
       self.setLayout(layout)
       
   def update_data(self, data: Dict):
       points = self._extract_points(data)
       if points:
           self.scene.update_skeleton(points)
           self.info_label.setText(f"Frame: {data.get('header', 'N/A')}")
           
   def _extract_points(self, data: Dict) -> List[QPointF]:
       # Placeholder implementation - update with actual MVN data processing
       points = []
       if 'payload' in data:
           raw_data = data['payload'].get('raw_data', b'')
           if raw_data:
               t = data.get('timestamp', 0)
               points = [
                   QPointF(100 * math.sin(t), 100 * math.cos(t)),
                   QPointF(100 * math.sin(t + 0.5), 100 * math.cos(t + 0.5)),
                   QPointF(100 * math.sin(t + 1.0), 100 * math.cos(t + 1.0))
               ]
       return points
       
   def resizeEvent(self, event):
       super().resizeEvent(event)
       self.view.setSceneRect(-self.width()/2, -self.height()/2,
                             self.width(), self.height())
