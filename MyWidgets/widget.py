from django import forms


class MyEditorWidget(forms.Textarea):
    class Media:
        css = { 'all' : ( 'css/ui-lightness/jquery-ui-1.8.23.css', 'js/markitup/skins/markitup/style.css', 'js/markitup/sets/default/style.css', 'css/markitup.css') }
        js = (
            'js/jquery-1.8.0.min.js',
            'js/jquery-ui-1.8.23.min.js',
            'js/markitup/jquery.markitup.js',
            'js/markitup/sets/default/set.js',
            'js/enable_editor.js',
        )

    def __init__(self, attrs={}):
        editorClass = ' myeditor'
        try:
            if editorClass not in attrs['class']:
                attrs['class'] += editorClass
        except KeyError:
            attrs['class'] = editorClass

        super(MyEditorWidget, self).__init__(attrs=attrs)
