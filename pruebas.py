import pytest
from unittest.mock import MagicMock, patch
from asistente import AsistenteVoz, Acciones, LecturaPDF, PageChatGPT
import time

# Mock de Acciones
@pytest.fixture
def mock_acciones():
    mock = MagicMock()
    mock.abrir_word = MagicMock()
    mock.abrir_excel = MagicMock()
    mock.abrir_powerpoint = MagicMock()
    mock.abrir_navegador = MagicMock()
    mock.abrir_chatgpt = MagicMock()
    mock.abrir_teams = MagicMock()
    mock.abrir_pdf = MagicMock()
    return mock

# Test 1: Verificar que procesar comando "abrir word" llama a la acción correspondiente
def test_procesar_comando_abrir_word(mock_acciones):
    # Crear el objeto de la clase AsistenteVoz con dependencias mockeadas
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    
    # Procesar el comando
    asistente.procesar_comando("abrir word")
    
    # Verificar que la acción de abrir Word se haya llamado
    mock_acciones.abrir_word.assert_called_once()

# Test 2: Verificar que procesar comando "empezar dictado" activa el dictado
def test_procesar_comando_empezar_dictado():
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    
    # Procesar el comando "empezar dictado"
    asistente.procesar_comando("empezar dictado")
    
    # Verificar que el dictado se ha activado
    assert asistente.dictado_activo is True

# Test 3: Verificar que procesar comando "terminar dictado" desactiva el dictado
def test_procesar_comando_terminar_dictado():
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    asistente.dictado_activo = True  # Simulamos que el dictado está activo
    
    # Procesar el comando "terminar dictado"
    asistente.procesar_comando("terminar dictado")
    
    # Verificar que el dictado se ha desactivado
    assert asistente.dictado_activo is False

# Test 4: Verificar que procesar comando "guardar documento word" llama a la función de guardar
@patch('pyautogui.typewrite')
@patch('pyautogui.press')
def test_guardar_documento_word(mock_press, mock_typewrite):
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    
    # Procesar el comando "guardar documento word"
    asistente.procesar_comando("guardar documento word test_documento")
    
    # Verificar que se haya llamado a pyautogui.typewrite con el nombre del archivo
    mock_typewrite.assert_any_call('test_documento.docx')
    # Verificar que se haya presionado la tecla 'enter'
    mock_press.assert_called_with('enter')

# Test 5: Verificar que procesar comando "guardar documento pdf" llama a la función de guardar
@patch('pyautogui.typewrite')
@patch('pyautogui.press')
def test_guardar_documento_pdf(mock_press, mock_typewrite):
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    
    # Procesar el comando "guardar documento pdf"
    asistente.procesar_comando("guardar documento pdf test_documento")
    
    # Verificar que se haya llamado a pyautogui.typewrite con el nombre del archivo
    mock_typewrite.assert_any_call('test_documento.pdf')
    # Verificar que se haya presionado la tecla 'enter'
    mock_press.assert_called_with('enter')

# Test 6: Verificar que el comando "abrir pdf" llama a la acción correspondiente
def test_procesar_comando_abrir_pdf(mock_acciones):
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    
    # Procesar el comando "abrir pdf"
    asistente.procesar_comando("abrir pdf")
    
    # Verificar que se haya llamado a LecturaPDF.abrir_pdf_desde_descargas
    LecturaPDF.abrir_pdf_desde_descargas.assert_called_once()

# Test 7: Verificar que procesar el comando "abrir último archivo listado" abre el último archivo
@patch.object(LecturaPDF, 'abrir_archivo_por_nombre')
def test_procesar_comando_abrir_ultimo_archivo(mock_abrir_archivo):
    # Simulamos que hay un archivo listado
    LecturaPDF.ultimo_archivo_listado = "ultimo_documento.pdf"
    
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    
    # Procesar el comando "abrir último archivo listado"
    asistente.procesar_comando("abrir último archivo listado")
    
    # Verificar que se haya llamado a la función de abrir el archivo listado
    mock_abrir_archivo.assert_called_with("ultimo_documento.pdf")

# Test 8: Verificar que procesar el comando "cerrar asistente virtual" detiene el asistente
def test_procesar_comando_cerrar_asistente():
    # Mock de la función de cierre de aplicación
    cerrar_app_callback = MagicMock()
    
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=cerrar_app_callback)
    
    # Procesar el comando "cerrar asistente virtual"
    asistente.procesar_comando("cerrar asistente virtual")
    
    # Verificar que el evento de detener el asistente ha sido activado
    assert asistente.detener_evento.is_set() is True
    # Verificar que se ha llamado al callback para cerrar la aplicación
    cerrar_app_callback.assert_called_once()

# Test 9: Verificar que el comando "empezar dictado" llama a la acción de dictado
@patch.object(Acciones, 'empezar_dictado')
def test_empezar_dictado(mock_empezar_dictado):
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    
    # Procesar el comando "empezar dictado"
    asistente.procesar_comando("empezar dictado")
    
    # Verificar que la acción de empezar dictado ha sido llamada
    mock_empezar_dictado.assert_called_once()

# Test 10: Verificar que el comando "terminar dictado" llama a la acción de terminar dictado
@patch.object(Acciones, 'terminar_dictado')
def test_terminar_dictado(mock_terminar_dictado):
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    
    # Procesar el comando "terminar dictado"
    asistente.procesar_comando("terminar dictado")
    
    # Verificar que la acción de terminar dictado ha sido llamada
    mock_terminar_dictado.assert_called_once()

# Test 11: Verificar que procesar el comando "abrir chat gpt" abre ChatGPT
@patch.object(PageChatGPT, 'activar_campo_busqueda')
def test_procesar_comando_abrir_chatgpt(mock_activar_campo_busqueda):
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    
    # Procesar el comando "abrir chat gpt"
    asistente.procesar_comando("abrir chat gpt")
    
    # Verificar que se ha llamado a PageChatGPT.activar_campo_busqueda
    mock_activar_campo_busqueda.assert_called_once()

# Test 12: Verificar que procesar el comando "abrir teams" abre Teams
def test_procesar_comando_abrir_teams(mock_acciones):
    asistente = AsistenteVoz(logger=MagicMock(), cerrar_app_callback=MagicMock())
    
    # Procesar el comando "abrir teams"
    asistente.procesar_comando("abrir teams")
    
    # Verificar que se ha llamado a Acciones.abrir_teams
    mock_acciones.abrir_teams.assert_called_once()