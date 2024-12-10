function getApiCookie() {
    const cookies = document.cookie.split(";"); // 獲取所有 Cookie，分號分隔
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // 檢查這個 Cookie 是否以指定的名稱開始
      if (cookie.startsWith("api=")) {
        return cookie.substring("api".length + 1); // 返回值
      }
    }
    return ""; // 如果找不到，返回空字串
}

function setApiCookie(value) {
    let days=7;
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000); // 設置過期時間
    const expires = "expires=" + date.toUTCString();
    document.cookie = `api=${value}; ${expires}; path=/`;
}

export {getApiCookie,setApiCookie};