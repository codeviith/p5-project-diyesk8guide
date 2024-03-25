/////////// WORKING NOW!!! updated user inactivity and timer reset w/o useCallback /////////////

import React, { createContext, useState, useEffect, useRef } from 'react';
import { useHistory } from 'react-router-dom';

export const AuthContext = createContext();

const INACTIVITY_TIMEOUT_VALUE = 3 * 60 * 1000;
const AUTO_LOGOUT_TIMEOUT_VALUE = 5 * 60 * 1000;
const COUNTDOWN_TO_LOGOUT = (AUTO_LOGOUT_TIMEOUT_VALUE - INACTIVITY_TIMEOUT_VALUE) / 1000;

export const AuthProvider = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [showInactivityModal, setShowInactivityModal] = useState(false);
    const [countdownTime, setCountdownTime] = useState(COUNTDOWN_TO_LOGOUT);

    const history = useHistory();
    const inactivityTimerRef = useRef(null);  // code for useRef to hold timer reference for inactivity
    const autoLogoutTimerRef = useRef(null);  // code for useRef to hold timer reference for autoLogout
    const countdownIntervalRef = useRef(null);  // code for useRef to hold timer reference for countdown

    const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://127.0.0.1:5555';


    const keepSessionAlive = async () => {
        const response = await fetch(`${backendUrl}/keep_session_alive`, {
            method: 'POST',
            credentials: 'include',
        });
        if (response.ok) {
            setShowInactivityModal(false);
            clearInterval(countdownIntervalRef.current);
            resetInactivityTimer();
        }
    };

    const logMeOut = async () => {
        const response = await fetch(`${backendUrl}/logout`, {
            method: 'POST',
            credentials: 'include',
        });
        if (response.ok) {
            setIsLoggedIn(false);
            setShowInactivityModal(false);
            clearInterval(countdownIntervalRef.current);  // code to clear countdown
            clearTimeout(inactivityTimerRef.current);  // code to clear inactivity timer
            clearTimeout(autoLogoutTimerRef.current);  // code to clear autologout timer
            history.push('/login');  // code to redirect to login page
        }
    };

    const startCountdown = () => {
        setCountdownTime(COUNTDOWN_TO_LOGOUT);
        clearInterval(countdownIntervalRef.current);
        countdownIntervalRef.current = setInterval(() => {
            setCountdownTime(prevTime => prevTime - 1);
        }, 1000);
    };

    function resetInactivityTimer() {
        clearTimeout(inactivityTimerRef.current);
        clearTimeout(autoLogoutTimerRef.current);
        clearInterval(countdownIntervalRef.current);

        inactivityTimerRef.current = setTimeout(() => {
            if (isLoggedIn) {
                setShowInactivityModal(true);
                startCountdown();  // code to start the countdown once modal has been shown to user
            }
        }, INACTIVITY_TIMEOUT_VALUE);

        autoLogoutTimerRef.current = setTimeout(() => {  // code to set up automatic logout after x minutes of inactivity
            if (isLoggedIn) {
                logMeOut();  // code to call on the logout function to log the user out
            }
        }, AUTO_LOGOUT_TIMEOUT_VALUE);
    }

    useEffect(() => {
        const checkLoginStatus = async () => {
            try {
                const response = await fetch(`${backendUrl}/check_session`, {
                    credentials: 'include',
                });
                const data = await response.json();
                setIsLoggedIn(data.logged_in);
            } catch (error) {
                console.error('Error checking login status:', error);
            }
        };

        checkLoginStatus();
    }, [backendUrl]);

    useEffect(() => {
        const handleUserActivity = () => resetInactivityTimer();

        window.addEventListener('mousemove', handleUserActivity);
        window.addEventListener('mousedown', handleUserActivity);
        window.addEventListener('keypress', handleUserActivity);
        window.addEventListener('scroll', handleUserActivity);

        resetInactivityTimer();  // code to initialize the timer

        return () => {  // code to cleanup event listeners
            window.removeEventListener('mousemove', handleUserActivity);
            window.removeEventListener('mousedown', handleUserActivity);
            window.removeEventListener('keypress', handleUserActivity);
            window.removeEventListener('scroll', handleUserActivity);
            clearTimeout(inactivityTimerRef.current);
            clearTimeout(autoLogoutTimerRef.current);
            clearInterval(countdownIntervalRef.current);
        };
    }, [isLoggedIn]); // code for isLoggedIn dependency to add/remove event listeners based on login status

    useEffect(() => {  // code to ensure timer is cleared on component unmount
        return () => {
            clearTimeout(inactivityTimerRef.current);
            clearTimeout(autoLogoutTimerRef.current);
            clearInterval(countdownIntervalRef.current);
        }
    }, []);


    return (
        <AuthContext.Provider value={{ isLoggedIn, setIsLoggedIn }}>
            {children}
            {showInactivityModal && (
                <div className="session-expiry-modal">
                    <p className="session-expiry-text">Your session is about to expire due to inactivity.</p>
                    <p className="session-expiry-text">Logging out in {countdownTime} seconds...</p>
                    <div className='buttons-container'>
                        <button className='keep-session-alive-button'
                            onClick={keepSessionAlive}
                        >
                            Keep Me Logged In
                        </button>
                        <button className='session-logout-button'
                            onClick={logMeOut}
                        >
                            Log Me Out
                        </button>
                    </div>
                </div>
            )}
        </AuthContext.Provider>
    );
};
