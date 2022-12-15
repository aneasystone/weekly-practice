package com.example;

import java.util.concurrent.locks.ReentrantLock;

public class DemoApp {

    static final ReentrantLock lock1 = new ReentrantLock();
    static final ReentrantLock lock2 = new ReentrantLock();

    public static void main(String[] args) throws Exception {
        
        Thread threada = new Thread(() -> {
            try {
                System.out.println("[Thread-A] I'm locking lock1");
                lock1.lock();
                System.out.println("[Thread-A] lock1 is locked");
                Thread.sleep(5000);
                System.out.println("[Thread-A] I'm locking lock2");
                lock2.lock();
                System.out.println("[Thread-A] lock2 is locked");
            } catch (Exception e) {
                System.out.println(e.getMessage());
            } finally {
                lock1.unlock();
                lock2.unlock();
                System.out.println("[Thread-A] lock1 and lock2 is unlocked");
            }
        });
        Thread threadb = new Thread(() -> {
            try {
                System.out.println("[Thread-B] I'm locking lock2");
                lock2.lock();
                System.out.println("[Thread-B] lock2 is locked");
                Thread.sleep(5000);
                System.out.println("[Thread-B] I'm locking lock1");
                lock1.lock();
                System.out.println("[Thread-B] lock1 is locked");
            } catch (Exception e) {
                System.out.println(e.getMessage());
            } finally {
                lock2.unlock();
                lock1.unlock();
                System.out.println("[Thread-B] lock2 and lock1 is unlocked");
            }
        });
        threada.setName("Thread-A");
        threada.start();
        threadb.setName("Thread-B");
        threadb.start();
    }
}
