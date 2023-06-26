$(window).on("load",function(){
    $(".preloader").fadeOut("slow");
});
var btc = document.getElementById("bitcoin");
var nem = document.getElementById("nem");
var eth = document.getElementById("ethereum");
var mon = document.getElementById("monero");
var lite = document.getElementById("litecoin");
var rip = document.getElementById("ripple");
var dash = document.getElementById("dash");


var settings = {
    "async": true,
    "scrossDomain": true,
    "url":"https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum%2Clitecoin%2Cripple%2Cdash%2Cnem%2Cmonero&vs_currencies=usd",
    "method":"GET",
    "headers":{}
}
$.ajax(settings).done(function(response){
    btc.innerHTML = response.bitcoin.usd;
    nem.innerHTML = response.nem.usd;
    eth.innerHTML = response.ethereum.usd;
    dash.innerHTML = response.dash.usd;
    lite.innerHTML = response.litecoin.usd;
    mon.innerHTML = response.monero.usd;
    rip.innerHTML = response.ripple.usd;
});
$('.alert').alert()
