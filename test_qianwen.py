import tempfile
import unittest
from pathlib import Path
from docx import Document
from qianwen_browser import read_export

class QianwenExportTests(unittest.TestCase):
    def export(self, lines):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        path=Path(temp.name)/'export.docx';doc=Document()
        for line in lines:doc.add_paragraph(line)
        doc.save(path);return path
    def test_preserves_all_paragraphs_and_speakers(self):
        p=self.export(['标题','2026年10月07日','发言人1   00:00','第一段。','继续讲话。','发言人2   00:12','第二段。'])
        result=read_export(p,20)
        self.assertEqual(result['segments'],[{'start':0,'end':12,'speaker':'发言人1','text':'第一段。\n继续讲话。'},{'start':12,'end':20,'speaker':'发言人2','text':'第二段。'}])
    def test_rejects_missing_timestamps(self):
        with self.assertRaises(ValueError):read_export(self.export(['只有正文']),20)
    def test_rejects_wrong_duration(self):
        with self.assertRaises(ValueError):read_export(self.export(['发言人1   01:00','正文']),20)
    def test_rejects_empty_segment(self):
        with self.assertRaises(ValueError):read_export(self.export(['发言人1   00:00']),20)

if __name__=='__main__':unittest.main()
