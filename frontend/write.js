const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault();
  try {
    const res = await fetch("/items", {
      method: "POST",
      body: new FormData(form),
    });
    const data = await res.json();
    if (data === "200") window.location.pathname = "/"; //정상처리되었을때 보여줄 창
  } catch (e) {
    console.error(e);
  }
};

form.addEventListener("submit", handleSubmitForm);
