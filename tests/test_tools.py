import unittest
import os
from agent.tools import code_editor

class TestCodeEditorTool(unittest.TestCase):
    def setUp(self):
        self.tool = code_editor.CodeEditorTool()

    def test_read_nonexistent_file(self):
        """Prueba la lectura de un archivo inexistente."""
        result = self.tool.run("archivo_inexistente.txt\nleer")
        self.assertIn("Archivo no encontrado", result)

    def test_write_and_read_file(self):
        filename = "test_file.txt"
        content = "Este es un contenido de prueba."
        write_result = self.tool.run(f"{filename}\nescribir\n```{content}```")
        self.assertIn("modificado correctamente", write_result)
        read_result = self.tool.run(f"{filename}\nleer")
        self.assertEqual(content, read_result)
        os.remove(filename)

    def test_invalid_action(self):
        result = self.tool.run("archivo.txt\naccion_invalida")
        self.assertEqual("Acción no válida. Debe ser 'leer' o 'escribir'.", result)

    def test_parse_query(self):
        tool = code_editor.CodeEditorTool()
        filename, action, code = tool._parse_query("test.py\nescribir\n```print('Hola')```")
        self.assertEqual(filename, "test.py")
        self.assertEqual(action, "escribir")
        self.assertEqual(code, "print('Hola')")

    def test_error_writing_file(self):
        tool = code_editor.CodeEditorTool()
        result = tool.run("/no/puedo/escribir/aqui.txt\nescribir\n```codigo```")
        self.assertTrue(result.startswith("Error al escribir en"))

    def test_read_existing_file(self):
        filename = "existing_test_file.txt"
        with open(filename, "w") as f:
            f.write("Contenido de prueba")
        result = self.tool.run(f"{filename}\nleer")
        self.assertEqual("Contenido de prueba", result)
        os.remove(filename)

    def test_write_new_file(self):
        filename = "new_test_file.txt"
        content = "Nuevo contenido de prueba"
        result = self.tool.run(f"{filename}\nescribir\n```{content}```")
        self.assertIn("modificado correctamente", result)
        read_result = self.tool.run(f"{filename}\nleer")
        self.assertEqual(content, read_result)
        os.remove(filename)

    def test_read_empty_file(self):
        filename = "empty_test_file.txt"
        open(filename, "w").close()
        result = self.tool.run(f"{filename}\nleer")
        self.assertEqual("", result)
        os.remove(filename)

    def test_write_invalid_content(self):
        filename = "invalid_content_file.txt"
        result = self.tool.run(f"{filename}\nescribir\ncontenido_invalido")
        self.assertIn("Error: Contenido inválido. Debe estar entre triples comillas.", result)

if __name__ == '__main__':
    unittest.main()