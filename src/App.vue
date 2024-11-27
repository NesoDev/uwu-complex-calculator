<template>
  <div id="app">
    <div class="front-app">
      <nav>
        <div id="logo-group">
          <img src="@/assets/logo-nav.png" alt="icon-app">
          <router-link to="/">Complex calculator</router-link>
        </div>
        <img src="@/assets/icon-github.png" alt="icon-png">
      </nav>
      <router-view />
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&display=swap');

#app {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.front-app {
  min-width: 320px;
  height: 90%;
  width: 90%;
  display: flex;
  box-sizing: border-box;
  flex-direction: column;
  justify-content: space-between;
  gap: 20px;
}


@media (min-width: 768px) {
  .front-app {
    width: 80%;
  }
}

@media (min-width: 1050px) {
  .front-app {
    width: 50%;
  }
}

@media (min-width: 1280px) {
  .front-app {
    width: 35%;
  }
}

nav {
  width: 100%;
  height: auto;
  background: linear-gradient(135deg, #3a2082, #191141, #241647);
  border-radius: 20px;
  padding: 10px 15px;
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 0;
}

#logo-group {
  width: auto;
  height: auto;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
}

#logo-group img {
  height: 30px;
}

nav a {
  font-size: 15px;
  font-weight: bold;
  color: #e2e2e2;
  text-decoration: none;
  font-family: "Fira Code", monospace;
}

#content {
  width: 100%;
  height: 100dvh;
  background: rgb(6, 6, 6);
}
</style>
