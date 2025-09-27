@extends('layouts.app')

@section('content')
<div class="container">
    <h1>Barcode Scanner</h1>
    <button id="start-scanner" class="btn btn-primary">Start Scanner</button>
    <video id="barcode-scanner" width="100%" style="display:none;"></video>
    <div id="scan-results" style="margin-top:20px;"></div>
</div>
@endsection

@section('scripts')
<script src="https://cdnjs.cloudflare.com/ajax/libs/quagga/0.12.1/quagga.min.js"></script>
<script src="{{ asset('js/barcode_scanner.js') }}"></script>
@endsection