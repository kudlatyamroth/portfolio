// ----------------------------------------------------------------------------
// markItUp!
// ----------------------------------------------------------------------------
// Copyright (C) 2011 Jay Salvat
// http://markitup.jaysalvat.com/
// ----------------------------------------------------------------------------
// Html tags
// http://en.wikipedia.org/wiki/html
// ----------------------------------------------------------------------------
// Basic set. Feel free to add more tags
// ----------------------------------------------------------------------------
$(document).ready(function() {
    var mySettings = {
        onShiftEnter:  {
            keepDefault:false,
            replaceWith:'<br />\n'
        },
        onCtrlEnter:  {
            keepDefault:false,
            openWith:'\n<p>',
            closeWith:'</p>'
        },
        onTab:  {
            keepDefault: false,
            replaceWith: '    '
        },
        markupSet:  [
            {name:'Bold', key:'B', openWith:'(!(<strong>|!|<b>)!)', closeWith:'(!(</strong>|!|</b>)!)' },
            {name:'Italic', key:'I', openWith:'(!(<em>|!|<i>)!)', closeWith:'(!(</em>|!|</i>)!)'  },
            {name:'Stroke through', key:'S', openWith:'<del>', closeWith:'</del>' },
            {separator:'---------------' },
            {name:'Bulleted List', openWith:'    <li>', closeWith:'</li>', multiline:true, openBlockWith:'<ul>\n', closeBlockWith:'\n</ul>'},
            {name:'Numeric List', openWith:'    <li>', closeWith:'</li>', multiline:true, openBlockWith:'<ol>\n', closeBlockWith:'\n</ol>'},
            {separator:'---------------' },
            {name:'Picture', key:'P', replaceWith:'<img src="[![Source:!:http://]!]" alt="[![Alternative text]!]" />' },
            {name:'Link', key:'L', openWith:'<a href="[![Link:!:http://]!]"(!( title="[![Title]!]")!)>', closeWith:'</a>', placeHolder:'Your text to link...' },
            {separator:'---------------' },
            {name:'Colors',
                className:'colors',
                openWith:'<span style="color: [![Color]!];">',
                closeWith:'</span>',
                    dropMenu: [
                        {name:'Yellow', openWith:'<span style="color: yellow;">',      closeWith:'</span>', className:"color_yellow" },
                        {name:'Orange', openWith:'<span style="color: orange;">',      closeWith:'</span>', className:"color_orange" },
                        {name:'Red',    openWith:'<span style="color: red;">',         closeWith:'</span>', className:"color_red" },

                        {name:'Blue',   openWith:'<span style="color: blue;">',        closeWith:'</span>', className:"color_blue" },
                        {name:'Purple', openWith:'<span style="color: purple;">',      closeWith:'</span>', className:"color_purple" },
                        {name:'Green',  openWith:'<span style="color: green;">',       closeWith:'</span>', className:"color_green" },

                        {name:'White',  openWith:'<span style="color: white;">',       closeWith:'</span>', className:"color_white" },
                        {name:'Gray',   openWith:'<span style="color: gray;">',        closeWith:'</span>', className:"color_gray" },
                        {name:'Black',  openWith:'<span style="color: black;">',       closeWith:'</span>', className:"color_black" }
                    ]
            },
            {separator:'---------------' },
            {name:'Clean', className:'clean', replaceWith:function(markitup) { return markitup.selection.replace(/<(.*?)>/g, "") } },
            {name:'Preview', className:'preview',  call:'preview'}
        ]
    }

    $('.myeditor').markItUp(mySettings);
    // You can add content from anywhere in your page
    // $.markItUp( { Settings } );
    $('.add').click(function() {
        $.markItUp({
                openWith:'<div class="markitup_editor">',
                closeWith:'<\/div>',
                placeHolder:"New content"
            }
        );
        return false;
    });
});
