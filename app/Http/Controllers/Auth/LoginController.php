<?php

namespace App\Http\Controllers\Auth;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\ValidationException;
use Illuminate\Foundation\Auth\ThrottlesLogins;

class LoginController extends Controller
{
    use ThrottlesLogins;

    /**
     * Maximum login attempts.
     */
    protected $maxAttempts = 3;

    /**
     * Lockout duration in minutes.
     */
    protected $decayMinutes = 5;

    /**
     * Handle a login request to the application.
     */
    public function login(Request $request)
    {
        $this->validateLogin($request);

        // Check for too many failed attempts
        if ($this->hasTooManyLoginAttempts($request)) {
            $this->fireLockoutEvent($request);

            throw ValidationException::withMessages([
                $this->username() => [trans('auth.throttle', ['seconds' => $this->decayMinutes * 60])],
            ]);
        }

        // Attempt to login the user
        if (Auth::attempt($request->only('email', 'password'))) {
            $this->clearLoginAttempts($request);
            return redirect()->intended('/dashboard');
        }

        // Increment failed attempts
        $this->incrementLoginAttempts($request);

        throw ValidationException::withMessages([
            $this->username() => [trans('auth.failed')],
        ]);
    }

    /**
     * Get the login username to be used by the controller.
     */
    public function username()
    {
        return 'email';
    }
}