var psw = document.getElementById('psw')
var rep_psw = document.getElementById('rep-psw')
var nam = document.getElementById('nam')
function alerted(){
	if (psw.value.length == 0) {
		return
	}
	else if (psw.value != rep_psw.value) {
		alert('Пароли не совпадают!');
	}
	else if (nam.value.charAt(0) != nam.value.charAt(0).toUpperCase()) {
		alert('Введите имя с заглавной буквы!');
	}

	else {
		alert('Регистрация прошла успешно!')
	}
}