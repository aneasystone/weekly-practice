package com.example.hello.locks;

import java.util.Comparator;
import java.util.List;
import java.util.concurrent.CountDownLatch;

import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooDefs;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.data.Stat;

public class LockService implements Watcher {

    private ZooKeeper zookeeper;
    private String lockPath;
    private CountDownLatch latch = new CountDownLatch(1);
    public LockService(ZooKeeper zookeeper, String lockPath) {
        this.zookeeper = zookeeper;
        this.lockPath = lockPath;
    }

    @Override
    public void process(WatchedEvent watchedEvent) {
        if (watchedEvent.getType() == Event.EventType.NodeDeleted) {
            latch.countDown();
        }
    }

    public void lock() {
        try {
			Stat stat = zookeeper.exists(this.lockPath, false);
			if (stat == null) {
				zookeeper.create(this.lockPath, null, ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
			}

            String currentNode = zookeeper.create(
                    this.lockPath + "/lock-", null, ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.EPHEMERAL_SEQUENTIAL);
            List<String> members = zookeeper.getChildren(this.lockPath, false);
            members.sort(Comparator.naturalOrder());

            // 当前节点序号最小，成功获取锁
            String lowestNode = this.lockPath + "/" + members.get(0);
            if (currentNode.equals(lowestNode)) {
                return;
            }

            // 取序号比自己稍小一点的节点，对该节点注册监听，当该节点删除时获取锁
            String lowerNode = null;
            for (int i = 1; i < members.size(); i++) {
                String node = this.lockPath + "/" + members.get(i);
                if (currentNode.equals(node)) {
                    lowerNode = this.lockPath + "/" + members.get(i-1);
                    break;
                }
            }
            if (lowerNode != null && zookeeper.exists(lowerNode, this) != null) {
                latch.await();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
	
    public static void main(String[] args) throws Exception {
		// 注意，这里的 sessionTimeout 设置的越久，获取锁所需的时间也就越久
        ZooKeeper zookeeper = new ZooKeeper("localhost:2181", 3000, null);
        LockService lockService = new LockService(zookeeper, "/locks");
        System.out.println("Try to get the lock");
        lockService.lock();
        System.out.println("Got the lock");
        Thread.sleep(Long.MAX_VALUE);
    }
}
