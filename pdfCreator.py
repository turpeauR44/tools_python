# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 20:25:08 2020

@author: turpeau.romain
"""


from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table as ReportTable, TableStyle, Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

class Pdf():
	def __init__(self, Dict):
		self.showgrid = Dict.get('showgrid',False)
		self.path = Dict['path']
		self.filename = Dict['filename']
		self.documentTitle = Dict.get('documentTitle','unknown')
		self.title = Text(Dict['title'])
		self.subTitle = Dict.get('subTitle', None)
		self.textLines = [Text(text) for text in Dict['textLines']]
		self.Fonts = Dict['Fonts']
		self.Images = [Image(image) for image in Dict.get('List_images',[])]
		self.Lines = [Line(line) for line in Dict.get('List_Lines',[])]
		self.Tables = [Table(table) for table in Dict.get('List_tables',[])]
		self.cur_table = ""

		self.Canvas = canvas.Canvas(self.path+self.filename)


		for font in self.Fonts:
			pdfmetrics.registerFont(TTFont(font['def'],'pdf\\fonts\\{}'.format(font['name'])))

		
	def create(self):
		self.Canvas.setTitle(self.documentTitle) 


		#add Images:
		for image in self.Images: self.add_Image(image)
		#add Lines:
		for line in self.Lines: self.add_Line(line)

		#create Title:
		self.add_Text(self.title)

		# create Texts:
		for txt in self.textLines:
			self.add_Text(txt)

	def save(self):
		self.Canvas.save()

	def add_Table(self,Dict):

		for table in self.Tables:
			if Dict['tab_name'] == table.name:
				self.cur_table = table

		data = Dict['data']
		f = ReportTable(data, colWidths=self.cur_table.colWidths )
		f.setStyle(TableStyle(self.cur_table.tableStyle))
		tw, th, = f.wrapOn(self.Canvas,self.cur_table.width, self.cur_table.height)
		f.drawOn(self.Canvas, self.cur_table.posX, self.cur_table.posY-th)

	def add_Text(self, obj):
		self.Canvas.setFont(obj.font, obj.size)
		self.Canvas.setFillColorRGB(obj.colorR,obj.colorG,obj.colorB)
		if obj.drawCentredString:
			self.Canvas.drawCentredString(obj.posX,obj.posY,obj.det)
		else:
			self.Canvas.drawText(obj.posX,obj.posY,obj.det)

	def add_Image(self,obj):
		self.Canvas.drawInlineImage(self.path+obj.det,obj.posX,obj.posY, width=obj.width, height = obj.height, preserveAspectRatio=obj.preserveAspectRatio)
     
	def add_Line(self,obj):
		self.Canvas.setFillColorRGB(obj.colorR,obj.colorG,obj.colorB)
		self.Canvas.line(obj.X1,obj.Y1,obj.X2,obj.Y2)


class Table():
	def __init__(self,Dict):
		self.name = Dict.get('tab_name', 'default')
		self.colWidths = Dict.get('colWidths', [])
		self.posX = Dict.get('posX', 0)
		self.posY = Dict.get('posY', 0)
		self.width = Dict.get('width', 585)
		self.height = Dict.get('height', 400)
		self.tableStyle = Dict.get('tableStyle', [])

class Text():
	def __init__(self,Dict):
		self.det = Dict.get('det', 'text')
		self.font = Dict.get('font', 'Colibri')
		self.size = Dict.get('size', 12)
		self.posX = Dict.get('posX', 0)
		self.posY = Dict.get('posY', 0)
		self.colorR = Dict.get('colorR', 0)
		self.colorG = Dict.get('colorG', 0)
		self.colorB = Dict.get('colorB', 0)
		self.drawCentredString = Dict.get('drawCentredString', False)

class Image():
	def __init__(self,Dict):
	    self.det = Dict.get('image', None)
	    self.posX = Dict.get('posX', 0)
	    self.posY = Dict.get('posY', 0)
	    self.width = Dict.get('width', None)
	    self.height = Dict.get('height', None)
	    self.preserveAspectRatio = Dict.get('preserveAspectRatio', True)

class Line():
	def __init__(self,Dict):
		self.coord = Dict.get('coord',[0,0,590,800])
		self.X1 = self.coord[0]
		self.Y1 = self.coord[1]
		self.X2 = self.coord[2]
		self.Y2 = self.coord[3]
		self.colorR = Dict.get('colorR', 0)
		self.colorG = Dict.get('colorG', 0)
		self.colorB = Dict.get('colorB', 0)

