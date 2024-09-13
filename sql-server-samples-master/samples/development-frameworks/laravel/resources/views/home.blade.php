@extends('layouts.master')

@section('content')
    <div class="text-center">
        <h1>Welcome to Laravel ToDo App</h1>
        <hr/>

        @include('partials.flash_notification')

        <p>For any query please contact</p>

        <h3>Meet Bhagdev</h3>
        <h4><a href="http://www.meetbhagdev">http://www.meetbhagdev.com</a></h4>
    </div>
@endsection
