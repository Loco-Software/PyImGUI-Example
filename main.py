import imgui
import glfw
import sys
import os
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer

if os.getenv("XDG_SESSION_TYPE") == "wayland":
    os.environ["XDG_SESSION_TYPE"] = "x11"


def window_loop():
    """Main Render Loop"""
    "Clear Colors"
    gl.glClearColor(0.1, 0.1, 0.1, 1)

    "Clear Window"
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    "Get I/O Information"
    io = imgui.get_io()

    "Check if Ctrl+Q was pressed, quit application if so"
    if io.key_ctrl and io.keys_down[glfw.KEY_Q]:
        sys.exit(0)

    "Create Main Window Menu Bar"
    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            "File Menu"
            clicked_quit, selected_quit = imgui.menu_item("Quit", "Ctrl+Q", False, True)

            if clicked_quit:
                sys.exit(0)

            "Close Menu"
            imgui.end_menu()
        "Close Main Menu Bar"
        imgui.end_main_menu_bar()

    "Welcome Message Box"
    imgui.begin("Welcome Message")

    "Welcome Message Text"
    imgui.text("Welcome to PyGuiBase")
    imgui.text("This is a Demo for PyImGUI")
    imgui.text("Developed by Loco Software")
    imgui.text("Available under the MIT License")
    imgui.text("URL: https://github.com/Loco-Software/PyGuiBase")

    "Close Welcome Message Box"
    imgui.end()


class GUIBase(object):
    """Example Class"""

    def impl_glfw_init(self):
        """Configured GLFW/OpenGL implementation for PyImGUI"""
        "Checks if GLFW is initialized after imgui.create_context()"
        if not glfw.init():
            print("Could not initialize OpenGL Context")
            sys.exit(1)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

        "Create Window"
        self.window = glfw.create_window(int(self.window_width), int(self.window_height), self.window_name, None, None)

        "Set Context as Current"
        glfw.make_context_current(self.window)

        "Check if Window exists"
        if not self.window:
            glfw.terminate()
            print("Could not Initialize Window")
            sys.exit()

    def render(self):
        """Render Function - not the Render Loop!"""
        "Poll Events and Process Input"
        glfw.poll_events()
        self.glfw_impl.process_inputs()

        "Create new Frame"
        imgui.new_frame()

        "Clear Colors"
        gl.glClearColor(0.1, 0.1, 0.1, 1)

        "Clear Window"
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        "Push Fonts if loaded"
        if self.font is not None:
            imgui.push_font(self.font)

        "Main Render Loop"
        window_loop()

        "Pop Font after Main Render"
        if self.font is not None:
            imgui.pop_font()

        "Render Window"
        imgui.render()

        "Pass Draw Data from ImGUI to GLFW/OpenGL"
        self.glfw_impl.render(imgui.get_draw_data())

        "Swap Display Buffer (Double Buffering)"
        glfw.swap_buffers(self.window)

    def __init__(self):
        """Constructor"""
        "Window Object"
        self.window = None

        "Window Height"
        self.window_height = 900

        "Window Width"
        self.window_width = 1600

        "Window Title"
        self.window_name = "PyGuiBase Example"

        "Create PyImGUI Context"
        imgui.create_context()

        "Configure GLFW/OpenGL implementation"
        self.impl_glfw_init()

        "Create GLFW/OpenGL Renderer"
        self.glfw_impl = GlfwRenderer(self.window)

        "Get I/O Information"
        io = imgui.get_io()

        "Load Font"
        self.font = io.fonts.add_font_from_file_ttf('./assets/fonts/font.ttf', 30)

        "Refresh Font Textures"
        self.glfw_impl.refresh_font_texture()

        "Render when no close command processed/passed"
        while not glfw.window_should_close(self.window):
            self.render()

        "Shutdown GLFW/OpenGL implementation"
        self.glfw_impl.shutdown()

        "Terminate GLFW/OpenGL"
        glfw.terminate()


def main():
    GUIBase()


if __name__ == "__main__":
    main()
