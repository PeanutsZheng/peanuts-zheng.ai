<template>
<transition name="fade" mode="out-in">
    <div class='Home'>
            <h1>Chat with peanutsZheng's AI</h1>

            <p>
                Here you can chat with Peanut or Aurora, which of them are all created by PeanutsZheng.<br>
                And you can also use Stable Diffusion model to generate images.
            </p>

            <p>
                If you want to know more about PeanutsZheng, please visit
                <a href="https://github.com/PeanutsZheng" target="_blank">peanutszheng's github</a>
            </p>

            <img src="../assets/peanutsZheng-logo.png" alt="peanutsZheng-Logo"
                title="peanutsZheng-logo" width="337" height="283">

            <p>
                The api keys are <em>http://localhost:5000/api</em> for chat
                and <em>http://localhost:5001/api</em> for draw.
            </p>
    </div>
</transition>
</template>

<script setup name='Home' lang='ts'>

</script>

<style scoped>
/* fade in and fade out */
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
    opacity: 0;
}
</style>