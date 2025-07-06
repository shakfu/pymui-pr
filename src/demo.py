import pymui

bg = [90, 95, 100]
LOGBUF_UPDATED = 0


def write_log(txt: str):
    print(txt)


def test_window(ctx: pymui.Context):
    # do windows
    if ctx.begin_window("Demo Window", pymui.Rect(40, 40, 300, 450)):
        win = ctx.mu_get_current_container()
        win.rect.w = max(win.rect.w, 240)
        win.rect.h = max(win.rect.h, 300)

        # window info
        if ctx.header("Window Info"):
            win = ctx.mu_get_current_container()
            ctx.layout_row(2, [54, -1], 0)
            ctx.label("Position:")
            ctx.label(f"{win.rect.x}, {win.rect.y}")
            ctx.label("Size:")
            ctx.label(f"{win.rect.w}, {win.rect.h}")

        # labels + buttons
        if ctx.header("Test Buttons", pymui.MU_OPT_EXPANDED):
            ctx.layout_row(3, [86, -110, -1], 0)
            ctx.label("Test buttons 1:")
            if ctx.button("Button 1"):
                write_log("Pressed button 1")
            if ctx.button("Button 2"):
                write_log("Pressed button 2")
            ctx.label("Test buttons 2:")
            if ctx.button("Button 3"):
                write_log("Pressed button 3")
            if ctx.button("Popup"):
                ctx.open_popup("Test Popup")
            if ctx.begin_popup("Test Popup"):
                ctx.button("Hello")
                ctx.button("World")
                ctx.end_popup()

        # tree
        if ctx.header("Tree and Text", pymui.MU_OPT_EXPANDED):
            ctx.layout_row(2, [140, -1], 0)
            ctx.layout_begin_column()
            if ctx.begin_treenode("Test 1"):
                if ctx.begin_treenode("Test 1a"):
                    ctx.label("Hello")
                    ctx.label("World")
                    ctx.end_treenode()

                if ctx.begin_treenode("Test 1b"):
                    if ctx.button("Button 1"):
                        write_log("Pressed button 1")
                    if ctx.button("Button 2"):
                        write_log("Pressed button 2")
                    ctx.end_treenode()
            ctx.end_treenode()

            if ctx.begin_treenode("Test 2"):
                ctx.layout_row(2, [54, 54], 0)
                if ctx.button("Button 3"):
                    write_log("Pressed button 3")
                if ctx.button("Button 4"):
                    write_log("Pressed button 4")
                if ctx.button("Button 5"):
                    write_log("Pressed button 5")
                if ctx.button("Button 6"):
                    write_log("Pressed button 6")
                ctx.end_treenode()

            if ctx.begin_treenode("Test 3"):
                checks = [1, 0, 1]
                ctx.checkbox("Checkbox 1", checks[0])
                ctx.checkbox("Checkbox 2", checks[1])
                ctx.checkbox("Checkbox 3", checks[2])
                ctx.end_treenode()

            ctx.layout_end_column()

            ctx.layout_begin_column()
            ctx.layout_row(1, [-1], 0)

            ctx.text(
                "Lorem ipsum dolor sit amet, consectetur adipiscing "
                "elit. Maecenas lacinia, sem eu lacinia molestie, mi risus faucibus "
                "ipsum, eu varius magna felis a nulla."
            )
            ctx.layout_end_column()

        # background color sliders
        if ctx.header("Background Color", pymui.MU_OPT_EXPANDED):
            ctx.layout_row(2, [-78, -1], 74)
            # sliders
            ctx.layout_begin_column()
            ctx.layout_row(2, [46, -1], 0)
            ctx.label("Red:")
            ctx.slider(bg[0], 0, 255)
            ctx.label("Green:")
            ctx.slider(bg[1], 0, 255)
            ctx.label("Blue:")
            ctx.slider(bg[2], 0, 255)
            ctx.layout_end_column()

            # color preview
            rect = ctx.layout_next()
            ctx.draw_rect(rect, pymui.Color(bg[0], bg[1], bg[2], 255))
            text = "{:02x}{:02x}{:02x}".format(bg[0], bg[1], bg[2])
            ctx.draw_control_text(
                text, rect, pymui.MU_COLOR_TEXT, pymui.MU_OPT_ALIGNCENTER
            )
    ctx.end_window()


def log_window(ctx: pymui.Context):
    if ctx.begin_window("Log Window", pymui.Rect(350, 40, 300, 200)):
        # output text panel
        ctx.layout_row(1, [-1], -25)
        ctx.begin_panel("Log Output")
        panel: pymui.Container = ctx.get_current_container()
        ctx.layout_row(1, [-1], -1)
        ctx.text(logbuf)
        ctx.end_panel()
        if LOGBUF_UPDATED:
            panel.scroll.y = panel.content_size.y
            LOGBUF_UPDATED = 0

        # input textbox + submit button
        submitted = 0
        ctx.layout_row(2, [-70, -1], 0)
        if ctx.textbox("", 128) and pymui.MU_RES_SUBMIT:
            ctx.set_focus(ctx.last_id)
            submitted = 1

        if ctx.button("Submit"):
            submitted = 1
        if submitted:
            write_log("hello")
        ctx.end_window()
