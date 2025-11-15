<template>
<div class='About'>
    <p>
        This is my <I>FIRST</I> vue project. <br>
        Honestly, I don't know what to write here.
        I'm trying to be a professional programmer but I'm not yet.
        I even don't sure if I'm goning to be a Front End Engineer.
        I'm just a guy who playing with code.
    </p>

    <p>
        This is my personal projcect, so I'm not going to tell you anything about me.
        But I'm going to tell you about my project. <br>
        It's a simple project, just has 4 views, you can chat with AI  or tell AI to 
        generate some images by your words. And you can toggle theme by click button. <br>
        I add many animate in the project to prevent flickering when loading a page.
        I used Vue3, TypeScript, Axios in this project. I install pinia but I didn't use it. <br>
        The back end servers is writen in Python, Flask. Just mentioning it, the parts of AI 
        are also from my another project. :p<br>
    </p>

    <p>
        In dir components, there are 2 components.
        I provide some method to use them. If you wanna use them, you can import them 
        in your project.<br>
        1. <I>CtrlPanel.vue</I> is a dynamically rendered control panel component. <br>
        You first need to import it in your project, then you add it's Ref constant 
        into your .html file or template tag. Then you can to add your widgets in 
        your .ts file or script tag and transmit them as porps to <I>CtrlPanel.vue</I>. 
        You can register widgets' event handler. You can alse use `getValues` or 
        `setValue` method to get / set widgets state.
        <br> <br>
        2. <I>Popup.vue</I> is an aesthetically pleasing message popup component. <br>
        You can use it to show some message to user. After import and add it's 
        Ref constant. You can use the `popup` method to show messages.
        </br></br>
    </p>

    <p>
        Author: PeanutsZheng <br>
        Date: 2025.11.13
    </p>
</div>
</template>

<script setup name='About' lang='ts'>

</script>

<style scoped>
.About {
    width: 90%;
    padding: 20px;
    font-size: 16px;
    line-height: 1.5;
    align-items: center;
}
</style>
