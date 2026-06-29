# Android 客户端面试题库（基于 Knowledge）

生成日期：2026-05-18

## 使用说明

本题库基于 Notion Knowledge 知识库递归读取和外部链接抽取整理，面向 Android 客户端候选人，不限定年限。题目按主题归类，难度分为 L1 实习/校招、L2 初中级、L3 中高级、L4 高级/资深。

每题统一包含：题号 / 难度 / 来源主题 / 面试题 / 考察点 / 参考答案 / 追问 / 评分标准。参考答案用于面试官校准，不建议作为唯一标准答案机械背诵。

## 读取覆盖记录

- Knowledge 根页：https://www.notion.so/Knowledge-8bd495756b3b43269f33fa88cb5dc7f5
- 编程语言：Kotlin、JVM、Java、数据结构
- 工程相关：常用设计模式、MVC/MVP/MVVM/MVI
- Android 基础：View 绘制、事件分发、四大组件、Binder、消息机制、多线程、ANR、OOM、异常捕获、LiveData、ViewModel、布局优化、SharedPreferences、FPS、动画、序列化、StrictMode、Flow、Channel、RecyclerView、APT、插件化、热修复、构建流程
- 计算机基础：局部性、IPC、加密、计算机网络
- 项目相关：ArchUnit、解耦、分层、TDD、单测、疑难 bug、换肤、脚本提速、多进程初始化、依赖链、CameraX 扫码
- 算法：二叉树遍历、排序、经典题目、剑指 Offer 目录

## 外部来源处理记录

- Android Developers - Enable app optimization with R8：https://developer.android.com/topic/performance/app-optimization/enable-app-optimization
- CSDN - Android 从点击应用图标到界面显示：https://blog.csdn.net/freekiteyu/article/details/79318031
- Gityuan - Handler 消息机制：http://gityuan.com/2015/12/26/handler-message/
- 掘金 - RecyclerView 复用机制：https://juejin.cn/post/6984974879296585764
- 掘金 - Android 动画原理：https://juejin.cn/post/7036986935545430030
- 掘金 - CameraX 扫码坐标映射：https://juejin.cn/post/7038559881187557406
- GitHub - CyC2018 CS-Notes 剑指 Offer：https://github.com/CyC2018/CS-Notes/blob/master/notes/%E5%89%91%E6%8C%87%20Offer%20%E9%A2%98%E8%A7%A3%20-%20%E7%9B%AE%E5%BD%95.md
- StrictMode Analysis：https://ericchows.github.io/Android-StrictMode-Analysis/
- 掘金/博客园/简书等外链若受登录、反爬或站点返回空壳限制，仅保留链接和从 Notion 笔记中可见的主题摘要，不复制外部正文。

## 图片处理记录

Notion 原页面中的图片大多是带签名的临时 URL，已在递归读取时识别并用于理解流程图、缓存图和坐标映射图。为了避免飞书文档长期失效和内容过重，正文优先落成文字化考点；需要查看原图时可回到对应 Notion 源页面。

## 一、语言基础、Java、Kotlin、JVM

### Q001 / L1 实习/校招 / Kotlin 扩展函数

- 面试题：Kotlin 扩展函数和扩展属性的实现原理是什么？
- 考察点：Kotlin 编译模型；静态分发；Java 调用方式。
- 参考答案：扩展函数本质上编译为静态方法，接收者对象会变成静态方法的第一个参数；扩展属性也只是生成 getter/setter 形式的静态访问方法，不会真的给目标类增加字段。扩展是静态分发，不能真正覆写成员函数，成员函数优先级高于扩展。
- 追问：如果 Java 调用 Kotlin 扩展函数会看到什么签名？为什么扩展函数无法访问 private 成员？
- 评分标准：能说出静态方法和接收者参数得 1 分；能解释静态分发、成员优先级、属性不持有状态得 2 分。

### Q002 / L1 实习/校招 / Kotlin lateinit

- 面试题：lateinit var 的运行时行为是什么？和可空类型有什么区别？
- 考察点：Kotlin 属性初始化；异常类型；空安全。
- 参考答案：lateinit 只适用于 var 引用类型，底层字段初始为 null，访问时会检查是否已初始化，未初始化会抛 UninitializedPropertyAccessException。它绕过了编译期必须初始化的要求，但不是可空类型，调用方不需要安全调用。
- 追问：lateinit 能用于 val、Int、Boolean 吗？为什么？
- 评分标准：能说出未初始化异常得 1 分；能说明引用类型、var 限制和空安全差异得 2 分。

### Q003 / L2 初中级 / Kotlin 委托

- 面试题：Kotlin by 委托在类委托和属性委托中分别做了什么？
- 考察点：语法糖反编译；代理模式；getValue/setValue。
- 参考答案：类委托会在生成类中保存被委托对象字段，并把接口方法转发给该对象；属性委托会把属性访问编译成对委托对象 getValue/setValue 的调用。lazy、observable、vetoable、Map 委托都属于属性委托的典型用法。
- 追问：lazy 的 SYNCHRONIZED、PUBLICATION、NONE 适合什么场景？
- 评分标准：能说出转发和 getValue/setValue 得 1 分；能结合 lazy 线程安全模式和实际场景得 2 分。

### Q004 / L2 初中级 / Kotlin inline

- 面试题：inline、noinline、crossinline、reified 分别解决什么问题？
- 考察点：高阶函数性能；非局部返回；泛型擦除。
- 参考答案：inline 把函数体和 lambda 调用点内联，减少 lambda 对象和虚调用开销；noinline 让某个 lambda 保持对象形态；crossinline 禁止非局部 return，适合 lambda 被二次封装或异步调用；reified 让内联函数中可以拿到泛型实参类型，缓解 JVM 泛型擦除。
- 追问：inline 是否越多越好？为什么会增加包体和编译成本？
- 评分标准：能解释四个关键字用途得 2 分；能说出适用边界和副作用得 3 分。

### Q005 / L2 初中级 / Kotlin object

- 面试题：object declaration、object expression、companion object 的差异是什么？
- 考察点：单例；匿名对象；Java 互操作。
- 参考答案：object declaration 用于声明单例，按需初始化且线程安全；object expression 用于创建匿名对象；companion object 是类关联的单例对象，可承载工厂方法或常量。加 @JvmStatic 后 Java 可像静态方法一样调用，否则要通过 Companion 实例访问。
- 追问：匿名对象作为 public 方法返回值时，为什么会丢失具体类型？
- 评分标准：能区分三种 object 得 1 分；能说明 Java 调用和可见性返回类型限制得 2 分。

### Q006 / L2 初中级 / Java 参数传递

- 面试题：Java 是值传递还是引用传递？修改对象字段和重新赋值参数有什么区别？
- 考察点：基础语义；引用值复制；面试陷阱。
- 参考答案：Java 只有值传递。基本类型传递的是值副本；对象参数传递的是引用值的副本。通过引用副本可以修改同一对象的字段，但把参数变量重新指向新对象不会影响调用方变量。
- 追问：String、Integer 这类对象在方法内修改为什么经常看起来像无效？
- 评分标准：能说出引用值副本得 1 分；能用对象字段修改和重新赋值对比说明得 2 分。

### Q007 / L1 实习/校招 / Java try finally

- 面试题：try/catch/finally 中 return 的执行顺序和风险是什么？
- 考察点：异常控制流；字节码复制 finally；代码规范。
- 参考答案：finally 通常都会执行；如果 finally 中也 return，会覆盖 try/catch 中的返回值和异常。finally 常用于释放锁、关闭资源，但不应写复杂控制流。编译后 finally 逻辑会被复制到多个出口附近。
- 追问：finally 一定会执行吗？System.exit 或进程崩溃时如何？
- 评分标准：能说出 finally return 覆盖风险得 1 分；能说明资源释放和例外情况得 2 分。

### Q008 / L2 初中级 / Java 反射

- 面试题：反射为什么慢？适合用在哪些场景？
- 考察点：Class 元数据；访问检查；动态调用。
- 参考答案：反射需要运行时解析 Class、Method、Field，绕过静态绑定并进行访问权限、安全检查、装箱拆箱等，JIT 优化空间较小。适合框架、序列化、依赖注入、插件化等需要运行时发现类型的场景，业务高频路径应缓存反射结果或改用编译期生成。
- 追问：EventBus 为什么引入编译期索引减少反射？
- 评分标准：能说明运行时解析和访问检查得 1 分；能给出缓存或 APT 替代方案得 2 分。

### Q009 / L2 初中级 / 单例模式

- 面试题：Java/Kotlin 单例的常见实现和线程安全点是什么？
- 考察点：DCL；volatile；静态内部类；Kotlin object。
- 参考答案：Java 常见实现有饿汉、懒汉、DCL、静态内部类。DCL 必须配合 volatile 防止指令重排序导致半初始化对象可见。静态内部类依赖类加载时机做到懒加载和线程安全。Kotlin object 由语言生成单例，初始化由类加载机制保障。
- 追问：DCL 不加 volatile 可能出现什么问题？
- 评分标准：能列举实现得 1 分；能解释 volatile 与类加载保障得 2 分。

### Q010 / L3 中高级 / 类加载

- 面试题：JVM 类加载流程、双亲委派和 Class.forName/loadClass 区别是什么？
- 考察点：类加载阶段；ClassLoader；初始化触发。
- 参考答案：类加载包括加载、验证、准备、解析、初始化和卸载。双亲委派先向父加载器委托，避免核心类被篡改并减少重复加载。Class.forName 默认会触发类初始化，loadClass 通常只加载不初始化。初始化阶段会执行静态变量赋值和 static 块，且由 JVM 保证线程安全。
- 追问：什么情况下需要打破双亲委派？Android 插件化如何处理？
- 评分标准：能讲清阶段和双亲委派得 2 分；能讲初始化触发和插件化类加载得 3 分。

### Q011 / L3 中高级 / JVM/JMM

- 面试题：JVM 运行时内存区和 Java 内存模型分别解决什么问题？
- 考察点：运行时内存；线程私有/共享；可见性。
- 参考答案：运行时内存区描述程序执行时数据放在哪里，包括堆、方法区、虚拟机栈、本地方法栈、程序计数器等；JMM 描述多线程下变量如何在主内存和工作内存间交互，解决原子性、可见性、有序性问题。volatile 解决可见性和禁止特定重排序，synchronized 同时提供互斥和可见性。
- 追问：final 字段为什么有特殊的可见性保证？
- 评分标准：能区分 JVM 内存区和 JMM 得 2 分；能结合 volatile/synchronized/final 得 3 分。

### Q012 / L3 中高级 / 垃圾回收

- 面试题：可达性分析、GC Roots 和常见回收算法如何理解？
- 考察点：GC Roots；分代；引用类型。
- 参考答案：可达性分析从 GC Roots 出发，无法到达的对象可被回收。GC Roots 包括栈中引用、静态字段、JNI 引用等。常见算法有标记清除、复制、标记整理；新生代常用复制算法，老年代更关注碎片和停顿。强软弱虚引用影响对象可达性和回收时机。
- 追问：为什么引用计数无法可靠处理循环引用？
- 评分标准：能说出 GC Roots 和可达性得 1 分；能结合分代与算法取舍得 2 分。

### Q013 / L3 中高级 / LeakCanary

- 面试题：LeakCanary 检测 Activity/Fragment 泄漏的核心链路是什么？
- 考察点：弱引用；ReferenceQueue；heap dump；最短路径。
- 参考答案：LeakCanary 监听 Activity/Fragment 生命周期，在销毁后用 KeyedWeakReference 关联对象和 ReferenceQueue；触发 GC 后若 key 仍未从 retainedKeys 移除，说明对象仍被强引用，随后 dump heap 并计算到 GC Roots 的最短强引用链。
- 追问：为什么不能只看对象是否 finalize？
- 评分标准：能说出弱引用队列和 retained key 得 2 分；能讲 heap 最短路径定位泄漏根因得 3 分。

### Q014 / L2 初中级 / 面向对象

- 面试题：封装、继承、多态、抽象各自解决什么问题？
- 考察点：OOP 基础；设计边界。
- 参考答案：封装隐藏内部状态并暴露稳定接口；继承表达 is-a 并复用父类能力；多态让同一接口在不同实现上表现不同；抽象提炼共性并约束实现。实际工程中要谨慎使用继承，过度继承会造成强耦合，组合通常更灵活。
- 追问：为什么“子类只是调用父类方法”可能应该改成组合？
- 评分标准：能解释四大特征得 1 分；能结合继承和组合取舍得 2 分。

### Q015 / L2 初中级 / 动态代理

- 面试题：Java 动态代理的原理和限制是什么？
- 考察点：Proxy；InvocationHandler；AOP。
- 参考答案：JDK 动态代理在运行时为接口生成代理类，代理方法统一转发到 InvocationHandler.invoke。它适合日志、埋点、RPC、Hook 等横切场景；限制是只能代理接口，无法直接代理普通类。类代理通常依赖 CGLib/ASM 或字节码插桩。
- 追问：Android 插件化 Hook startActivity 为什么会用动态代理？
- 评分标准：能说出 Proxy 和 InvocationHandler 得 1 分；能说明接口限制和 Hook 场景得 2 分。

## 二、数据结构与集合

### Q016 / L1 实习/校招 / String/StringBuilder/StringBuffer

- 面试题：String、StringBuilder、StringBuffer 的差异是什么？
- 考察点：不可变对象；线程安全；性能。
- 参考答案：String 不可变，拼接会产生新对象或被编译器优化；StringBuilder 可变且非线程安全，适合单线程拼接；StringBuffer 方法加 synchronized，线程安全但开销更高。
- 追问：Kotlin 字符串模板在循环里大量拼接应该注意什么？
- 评分标准：能说出可变性和线程安全得 1 分；能结合场景选择得 2 分。

### Q017 / L2 初中级 / HashMap

- 面试题：HashMap put/get、扰动函数和扩容迁移的核心逻辑是什么？
- 考察点：数组+链表/红黑树；哈希寻址；resize。
- 参考答案：HashMap 用 table 数组承载 Node，索引通常是 (n-1)&hash，hash 会做高低位扰动以降低碰撞。put 时定位桶，空桶直接放，冲突则链表或红黑树处理；负载超过阈值 resize。JDK8 扩容时元素要么留在原索引，要么移动到原索引+旧容量。
- 追问：为什么容量通常保持 2 的幂？
- 评分标准：能说出结构和索引计算得 1 分；能解释扰动、树化、扩容迁移得 2 分。

### Q018 / L2 初中级 / ConcurrentHashMap

- 面试题：ConcurrentHashMap 1.7 和 1.8 的并发控制差异是什么？
- 考察点：Segment；CAS；synchronized；红黑树。
- 参考答案：JDK7 用 Segment 分段锁，每个 Segment 维护一部分桶；JDK8 取消 Segment 主体结构，使用 CAS 初始化/插入空桶，桶级 synchronized 处理冲突，并在链表过长时树化。粒度更细，空间和并发性能更好。
- 追问：为什么 Hashtable 粒度更粗？
- 评分标准：能说出 Segment 与桶级锁差异得 1 分；能说明 CAS 和树化得 2 分。

### Q019 / L2 初中级 / LinkedHashMap/LruCache

- 面试题：Android LruCache 为什么常用 LinkedHashMap 实现？
- 考察点：访问顺序链表；淘汰策略；缓存大小。
- 参考答案：LinkedHashMap 在 HashMap 基础上维护双向链表，可按插入顺序或访问顺序排序。LruCache 设置 accessOrder=true，每次 get/put 会把节点移到尾部；trimToSize 时淘汰链表头部最久未访问元素，并通过 sizeOf 自定义权重。
- 追问：图片缓存 sizeOf 应该按对象个数还是内存大小？
- 评分标准：能说出 accessOrder 和头部淘汰得 1 分；能结合图片缓存权重和回调得 2 分。

### Q020 / L1 实习/校招 / 队列/栈/堆

- 面试题：队列、栈、堆的典型特性和 Java/Kotlin 常用实现是什么？
- 考察点：FIFO；LIFO；优先级队列。
- 参考答案：队列是 FIFO，可用 LinkedList、ArrayDeque；栈是 LIFO，推荐 ArrayDeque 而不是老的 Stack；堆通常用 PriorityQueue，默认小顶堆，可通过 Comparator 构造大顶堆。
- 追问：Top K 用小顶堆还是大顶堆？为什么？
- 评分标准：能说出三类结构特性得 1 分；能结合 Top K 选堆得 2 分。

### Q021 / L2 初中级 / SparseArray

- 面试题：SparseArray 相比 HashMap<Int, Object> 的优势和边界是什么？
- 考察点：Android 内存优化；二分查找；装箱。
- 参考答案：SparseArray 用两个数组分别保存有序 int key 和 value，通过二分查找定位，避免 Integer 装箱和 HashMap 节点对象，适合 Android 小规模 int key 映射。数据量很大或频繁随机插入时，数组移动和二分成本可能不如 HashMap。
- 追问：LongSparseArray、ArrayMap 适合什么场景？
- 评分标准：能说出避免装箱和双数组得 1 分；能说明小数据量边界得 2 分。

### Q022 / L2 初中级 / 深拷贝/浅拷贝

- 面试题：深拷贝和浅拷贝的区别是什么？Android 中常见风险在哪里？
- 考察点：对象图；可变引用；数据隔离。
- 参考答案：浅拷贝只复制当前对象字段，引用字段仍指向同一对象；深拷贝会递归复制被引用对象，使副本和原对象互不影响。Android 中列表数据、UI 状态、Intent 参数或缓存对象如果浅拷贝，可能产生串改和并发问题。
- 追问：Parcelable 传递对象是否一定是深拷贝？
- 评分标准：能说出引用共享得 1 分；能结合可变对象和跨组件传递风险得 2 分。

### Q023 / L2 初中级 / PriorityQueue

- 面试题：PriorityQueue 的排序语义是什么？为什么遍历不等于有序输出？
- 考察点：堆结构；peek/poll；Comparator。
- 参考答案：PriorityQueue 保证队头是当前优先级最高或最低的元素，但内部数组不是全局有序。只有连续 poll 才能得到优先级顺序。默认自然序是小顶堆，传入反向 Comparator 可变成大顶堆。
- 追问：如果 Comparator 写成 o2-o1 有什么溢出风险？
- 评分标准：能说出队头有序和内部非全局有序得 1 分；能指出 Comparator 溢出得 2 分。

### Q024 / L3 中高级 / 集合并发

- 面试题：为什么普通集合在多线程下会出问题？如何选择同步策略？
- 考察点：可见性；结构修改；fail-fast。
- 参考答案：普通 HashMap、ArrayList 并发读写可能产生数据丢失、结构损坏、可见性问题。选择策略要看读写比例和一致性要求：外部锁适合小范围临界区；ConcurrentHashMap 适合高并发 map；CopyOnWriteArrayList 适合读多写少；不可变快照适合状态流转。
- 追问：fail-fast 是线程安全保证吗？
- 评分标准：能说出结构和可见性问题得 1 分；能按场景选容器得 2 分。

## 三、Android 系统机制

### Q025 / L3 中高级 / 应用启动

- 面试题：从点击桌面图标到首个 Activity 显示，中间经过哪些进程和关键对象？
- 考察点：Launcher；AMS；Zygote；ActivityThread；Window。
- 参考答案：Launcher 通过 Binder 请求 system_server 中 AMS 启动 Activity；若进程不存在，AMS 通过 socket 请求 Zygote fork 应用进程；应用进程进入 ActivityThread.main，创建主 Looper 并 attach 到 AMS；AMS 发送 bindApplication，应用创建 Application、安装 ContentProvider 后调用 Application.onCreate；随后 scheduleLaunchActivity，创建 Activity、PhoneWindow/DecorView，resume 时通过 WindowManager 创建 ViewRootImpl 并触发绘制。
- 追问：Launcher 启动和应用内启动 Activity 有什么不同？
- 评分标准：能说出四个进程和 Binder/socket 得 2 分；能串起 Application、Provider、Activity、ViewRootImpl 得 3 分。

### Q026 / L3 中高级 / 四大组件

- 面试题：Application、ContentProvider、Activity、Service、Receiver 的创建顺序如何？
- 考察点：ActivityThread；组件冷启动；初始化时机。
- 参考答案：冷启动时 handleBindApplication 会创建 Application Context 并调用 attachBaseContext，安装 ContentProvider 并先执行 Provider.onCreate，之后调用 Application.onCreate。Activity、Service、Receiver 由 AMS 后续调度到 ActivityThread 的对应 handle 方法中创建。广播或服务冷启动也会先确保 Application 可用，再实例化目标组件。
- 追问：为什么 ContentProvider 常被用作库初始化入口？风险是什么？
- 评分标准：能说出 Provider 早于 Application.onCreate 得 2 分；能说明初始化风险和多进程影响得 3 分。

### Q027 / L2 初中级 / Service

- 面试题：startService、bindService 混用时生命周期如何结束？
- 考察点：Service 生命周期；绑定计数；stop 条件。
- 参考答案：仅 startService 时，需要 stopService 或 stopSelf 结束；仅 bindService 时，所有 client unbind 后可结束；两者混用时，需要所有绑定解绑且 stopService/stopSelf 已发生，Service 才会销毁。onCreate 只执行一次，onStartCommand 可多次，onBind 首次绑定回调。
- 追问：START_STICKY 和 START_REDELIVER_INTENT 怎么选？
- 评分标准：能说出三种结束条件得 1 分；能解释 onStartCommand 返回策略得 2 分。

### Q028 / L2 初中级 / BroadcastReceiver

- 面试题：静态广播、动态广播、有序广播、本地广播的差异是什么？
- 考察点：注册时机；AMS 分发；安全边界。
- 参考答案：静态广播在安装时由 PMS 解析注册，动态广播通过 ContextImpl 到 AMS 注册。普通广播并发分发，有序广播按优先级串行传递且可设置结果或中断。本地广播仅应用内分发，安全性和效率更好，但现在很多场景可用显式回调、Flow 或事件总线替代。
- 追问：广播冷启动进程时，Receiver.onReceive 前会不会创建 Application？
- 评分标准：能区分注册和分发类型得 1 分；能说出冷启动创建链路得 2 分。

### Q029 / L3 中高级 / ContentProvider

- 面试题：ContentProvider 的 onCreate 和 query/insert/update/delete 分别运行在哪些线程？
- 考察点：主线程；Binder 线程池；同进程调用。
- 参考答案：Provider.onCreate 运行在 Provider 所在进程主线程，因为它在 bindApplication 流程中安装。query/insert/update/delete 取决于调用场景：同进程调用通常在调用线程执行；跨进程调用由 Provider 所在进程 Binder 线程池处理。耗时数据库操作必须注意线程和并发。
- 追问：Provider 初始化里做重 IO 会造成什么问题？
- 评分标准：能区分 onCreate 与 CRUD 线程得 2 分；能结合跨进程 Binder 线程池和 ANR 风险得 3 分。

### Q030 / L4 高级/资深 / Binder

- 面试题：Binder 为什么通常被称为一次拷贝？mmap 在其中起什么作用？
- 考察点：Linux IPC；用户态/内核态；Binder 驱动。
- 参考答案：Binder 通过驱动管理跨进程通信，Service 端把一块内核缓冲区 mmap 到自身用户空间，Client 数据从用户空间拷贝到内核缓冲区后，Server 可在映射区域读取，减少传统 IPC 中内核到用户态的二次拷贝。Binder 还提供对象引用、死亡通知、线程池等上层语义。
- 追问：为什么 Binder 仍然有 1MB 左右事务缓冲限制？
- 评分标准：能说明 mmap 和一次拷贝得 2 分；能说出事务限制、线程池、死亡通知得 3 分。

### Q031 / L3 中高级 / Binder oneway

- 面试题：Binder oneway 的语义和风险是什么？
- 考察点：异步 Binder；事务队列；回调设计。
- 参考答案：oneway 表示调用方发起异步事务后不等待返回，适合通知类调用。但它不是无限并发，事务仍会进入目标进程 Binder 队列，过量 oneway 可能堆积导致阻塞或丢响应。需要结果时应设计 callback 或双向 Binder，同时注意 RemoteCallbackList 管理死亡和并发。
- 追问：oneway 是否一定运行在不同线程？
- 评分标准：能说出异步不等于无成本得 2 分；能讨论队列堆积和 callback 管理得 3 分。

### Q032 / L3 中高级 / Handler/Looper

- 面试题：Handler、Looper、MessageQueue、Message 的协作流程是什么？
- 考察点：线程消息循环；ThreadLocal；dispatch。
- 参考答案：Looper.prepare 在当前线程创建 Looper 并保存到 ThreadLocal，Looper.loop 不断从 MessageQueue 取消息。Handler 发送 Message 时把 target 指向自己并按 when 入队；取出消息后由 target.dispatchMessage 分发，优先 callback，其次 Handler.Callback，最后 handleMessage。主线程 Looper 在 ActivityThread.main 创建。
- 追问：为什么子线程默认不能直接创建 Handler？
- 评分标准：能说出四者关系得 1 分；能讲 dispatch 优先级和 ThreadLocal 得 2 分。

### Q033 / L3 中高级 / MessageQueue

- 面试题：MessageQueue 没消息或队头是延迟消息时，线程处于什么状态？如何被唤醒？
- 考察点：nativePollOnce；epoll；延迟消息。
- 参考答案：MessageQueue.next 会计算下一条消息到期时间。没有消息时可能无限等待，队头是延迟消息时按超时时间等待；底层通过 nativePollOnce 让线程休眠，不占用 CPU。有新消息入队且需要提前执行时会 nativeWake 唤醒。Java 线程状态通常表现为 waiting/timed waiting。
- 追问：IdleHandler 在什么时机执行？
- 评分标准：能说出休眠等待和唤醒得 1 分；能结合延迟消息和 IdleHandler 得 2 分。

### Q034 / L4 高级/资深 / 同步屏障

- 面试题：同步屏障和异步消息解决了什么问题？
- 考察点：View 绘制优先级；MessageQueue barrier。
- 参考答案：同步屏障是插入 MessageQueue 的特殊节点，阻塞普通同步消息，只允许异步消息越过屏障执行。ViewRootImpl.scheduleTraversals 会插入同步屏障并通过 Choreographer 注册 traversal，使输入、动画、绘制在下一帧获得更高优先级。绘制完成后移除屏障。
- 追问：如果屏障未移除会发生什么？
- 评分标准：能说出屏障只放行异步消息得 2 分；能联系 ViewRootImpl/Choreographer 得 3 分。

### Q035 / L3 中高级 / SharedPreferences

- 面试题：SharedPreferences 是线程安全吗？进程安全吗？commit/apply 差异是什么？
- 考察点：内存缓存；磁盘写入；多进程一致性。
- 参考答案：SP 内部大量使用 synchronized，同进程线程安全；但不是进程安全，MODE_MULTI_PROCESS 只通过文件时间和大小尝试重新加载，无法保证实时同步，频繁跨进程读写可能损坏数据。apply 先同步写内存，再异步写磁盘；commit 同步等待磁盘写入并返回结果。SP 文件过大会导致首次加载或全量写回阻塞。
- 追问：为什么不建议用 SP 做 IPC？
- 评分标准：能说出线程安全非进程安全得 1 分；能说明 apply/commit 和文件过大风险得 2 分。

### Q036 / L2 初中级 / 序列化

- 面试题：Serializable 和 Parcelable 的差异是什么？
- 考察点：反射；Parcel；组件传参。
- 参考答案：Serializable 是 Java 标准接口，实现简单但依赖反射，性能和临时对象开销更大；Parcelable 是 Android 专用机制，需要手写 writeToParcel/CREATOR，但更高效，适合 Activity/Service 间传递对象。跨平台持久化或网络传输不应依赖 Parcelable。
- 追问：Parcelable 里写入字段顺序为什么重要？
- 评分标准：能说出实现成本和性能差异得 1 分；能结合组件传参场景得 2 分。

### Q037 / L3 中高级 / Android 构建

- 面试题：minSdk、targetSdk、compileSdk 各自影响什么？Android 构建主要流程是什么？
- 考察点：SDK 兼容；AAPT/AIDL/Javac/D8/R8；签名。
- 参考答案：minSdk 决定最低可安装系统和 API 调用约束；compileSdk 决定编译时 API 和 lint/警告；targetSdk 告诉系统应用已适配的行为版本，影响运行时兼容策略。构建流程包括资源编译生成 R、AIDL、Java/Kotlin 编译、R8 shrink/obfuscate/optimize、D8/R8 生成 dex、打包、签名、zipalign。
- 追问：为什么 targetSdk 升级经常需要专项验证？
- 评分标准：能区分三类 SDK 得 1 分；能串起构建链路和 R8 作用得 2 分。

### Q038 / L3 中高级 / 插件化

- 面试题：插件 Activity 没在宿主 Manifest 注册，如何绕过 AMS 校验并恢复真实 Activity？
- 考察点：占坑 Activity；Hook AMS；ActivityThread H。
- 参考答案：常见方案是 Manifest 中预注册占坑 Activity。启动前 Hook ActivityManager，把插件 Intent 替换为占坑 Intent 并保存原始 Intent；AMS 校验通过后，应用进程 ActivityThread 收到 LAUNCH_ACTIVITY，在 Handler.Callback 或对应生命周期入口中把 Intent 恢复为插件 Activity。类加载用 DexClassLoader，多 ClassLoader 隔离或合并 dexElements；资源通过解析插件 APK 获取 Resources。
- 追问：Android 版本升级对 Hook 点有什么影响？
- 评分标准：能说出占坑与恢复得 2 分；能补充 ClassLoader 和资源加载得 3 分。

### Q039 / L3 中高级 / 热修复

- 面试题：代码、资源、so 热修复的基本思路分别是什么？
- 考察点：DexClassLoader；AssetManager；native lib。
- 参考答案：代码修复常用类加载方案，把 patch dex 插入 dexElements 前面，重启后优先加载补丁类；资源修复可反射创建 AssetManager 并 addAssetPath，再替换 Resources/Theme 的 mAssets；so 修复可优先 System.load 补丁路径或注入 nativeLibraryPath。不同方案在即时性、兼容性、稳定性上取舍明显。
- 追问：热修复和插件化的目标与风险有什么不同？
- 评分标准：能说出三类修复得 2 分；能讨论重启、兼容和回滚风险得 3 分。

## 四、UI、View、事件、动画

### Q040 / L3 中高级 / setContentView/ViewRootImpl

- 面试题：setContentView 到 ViewRootImpl.requestLayout 之间发生了什么？
- 考察点：PhoneWindow；DecorView；WindowManagerGlobal。
- 参考答案：Activity.setContentView 会委托 PhoneWindow 安装 DecorView 并把布局 inflate 到 content 区域。Activity resume 后 DecorView 被添加到 WindowManager，WindowManagerGlobal.addView 创建 ViewRootImpl，setView 后触发 requestLayout，最终通过 Choreographer 在下一帧执行 performTraversals。
- 追问：为什么 onCreate 里 getWidth 常为 0？
- 评分标准：能说出 PhoneWindow/DecorView/ViewRootImpl 得 2 分；能联系 requestLayout 和下一帧遍历得 3 分。

### Q041 / L3 中高级 / View 绘制

- 面试题：measure、layout、draw 的职责分别是什么？requestLayout 和 invalidate 差异是什么？
- 考察点：View 树遍历；测量缓存；重绘。
- 参考答案：measure 决定尺寸，layout 决定位置，draw 负责绘制。requestLayout 标记布局请求，可能触发 measure/layout/draw；invalidate 只标记脏区重绘，通常不重新测量布局；postInvalidate 可从非 UI 线程请求重绘。实际是否完整执行受标记位、父子关系和硬件加速影响。
- 追问：View 的 measuredWidth 和 width 何时不同？
- 评分标准：能说出三阶段职责得 1 分；能区分 requestLayout/invalidate 得 2 分。

### Q042 / L4 高级/资深 / Choreographer/VSync

- 面试题：Choreographer 如何把输入、动画、绘制串到一帧里？
- 考察点：VSync；CallbackQueue；Traversal。
- 参考答案：Choreographer 是线程内单例，监听 VSync 后按 callback 类型执行队列，典型包括 INPUT、ANIMATION、TRAVERSAL、COMMIT。ViewRootImpl.scheduleTraversals 把 traversal runnable 注册进 Choreographer，下一帧到来时执行 performTraversals。动画和 FPS 监控也通过 postFrameCallback 在帧回调中推进。
- 追问：为什么同一线程一个 Choreographer 足够？
- 评分标准：能说出四类 callback 和 VSync 得 2 分；能联系绘制、动画、FPS 得 3 分。

### Q043 / L3 中高级 / 事件分发

- 面试题：一次触摸事件从硬件到 View 的分发链路是什么？
- 考察点：InputReader/InputDispatcher；ViewRootImpl；dispatchTouchEvent。
- 参考答案：输入事件经系统输入管线到应用 ViewRootImpl，再到 DecorView、Activity.dispatchTouchEvent、Window、ViewGroup、View。ViewGroup 可在 dispatch 中判断目标子 View、调用 onInterceptTouchEvent 决定是否拦截；View 中 OnTouchListener 优先于 onTouchEvent，onClick 基于 ACTION_UP 触发。
- 追问：如果 ACTION_DOWN 没有 View 消费，后续 MOVE/UP 会怎样？
- 评分标准：能说出分发链路和 ViewGroup/View 优先级得 2 分；能说明 DOWN 消费对后续事件的影响得 3 分。

### Q044 / L3 中高级 / 滑动冲突

- 面试题：外部拦截和内部拦截分别怎么处理滑动冲突？
- 考察点：onInterceptTouchEvent；requestDisallowInterceptTouchEvent；ACTION_CANCEL。
- 参考答案：外部拦截由父容器在 onInterceptTouchEvent 中根据方向/边界决定是否拦截；内部拦截由子 View 先 requestDisallowInterceptTouchEvent(true)，在需要父容器接管时再放开。若父容器中途拦截，子 View 会收到 ACTION_CANCEL，父容器接管后续事件。
- 追问：为什么 DOWN 事件通常不建议拦截？
- 评分标准：能说出两种拦截策略得 1 分；能说明中途拦截和 CANCEL 得 2 分。

### Q045 / L3 中高级 / RecyclerView

- 面试题：RecyclerView 的四级缓存和复用优先级是什么？
- 考察点：Scrap；CacheView；ViewCacheExtension；RecycledViewPool。
- 参考答案：RecyclerView 复用主要涉及 changed/attached scrap、mCachedViews、ViewCacheExtension、RecycledViewPool。Scrap 和 mCachedViews 更偏精准复用，可能不需要重新 bind；RecycledViewPool 按 itemType 存放已清理 ViewHolder，取出后需要重新绑定。滑动时优先缓存离屏 ViewHolder 到 mCachedViews，满了再进 pool。
- 追问：stableId 对复用和动画有什么帮助？
- 评分标准：能说出缓存层级得 2 分；能说明哪些需要 rebind 和局部更新价值得 3 分。

### Q046 / L2 初中级 / 布局优化

- 面试题：ViewStub 和 AsyncLayoutInflater 分别适合解决什么问题？
- 考察点：延迟加载；异步 inflate；限制。
- 参考答案：ViewStub 是 0 尺寸、不绘制的占位 View，首次 setVisible 或 inflate 时替换成真实布局，只能 inflate 一次，适合低频出现的复杂区域。AsyncLayoutInflater 把 inflate 放到单独线程，完成后回主线程回调，适合解析成本高但构造过程不依赖主线程的布局；它不能直接设置 Factory，失败会回主线程重试。
- 追问：为什么 AsyncLayoutInflater inflate(layout,parent,false) 后要手动 addView？
- 评分标准：能说出两者用途得 1 分；能指出限制和线程风险得 2 分。

### Q047 / L3 中高级 / 属性动画

- 面试题：ValueAnimator 如何按帧推进动画？
- 考察点：AnimationHandler；Choreographer；插值器。
- 参考答案：ValueAnimator.start 会把自身作为 AnimationFrameCallback 注册到线程内 AnimationHandler。AnimationHandler 首次通过 Choreographer.postFrameCallback 请求下一帧；每帧 doFrame 遍历动画 callback，ValueAnimator 根据当前时间计算 fraction，经 Interpolator 转换后更新 PropertyValuesHolder 并回调 onAnimationUpdate。动画结束后从列表移除。
- 追问：ObjectAnimator 比 ValueAnimator 多做了什么？
- 评分标准：能说出 Choreographer 驱动和 fraction 计算得 2 分；能解释 AnimationHandler 线程内单例得 3 分。

### Q048 / L2 初中级 / FPS 监控

- 面试题：如何用 Choreographer 监控 FPS 和掉帧？
- 考察点：FrameCallback；帧间隔；掉帧数。
- 参考答案：通过 Choreographer.postFrameCallback 注册 FrameCallback，每帧记录 frameTimeNanos，与上一帧时间差比较。理想 60Hz 下一帧间隔约 16.6ms，差值除以标准间隔可估算 skipped frames。回调中再次 postFrameCallback 形成持续监控。
- 追问：为什么只看平均 FPS 不足以定位卡顿？
- 评分标准：能说出帧回调和间隔计算得 1 分；能补充长帧、主线程任务和 trace 分析得 2 分。

### Q049 / L3 中高级 / CameraX 坐标映射

- 面试题：扫码识别返回的是裁剪图坐标，如何映射到屏幕预览坐标？
- 考察点：矩阵变换；裁剪；预览比例。
- 参考答案：先明确源坐标系是裁剪/预处理后的图像，目标坐标系是 PreviewView 或取景框。用 Matrix.setPolyToPoly 或 setRectToRect 描述源矩形到目标矩形的变换，再用 mapPoints 把二维码顶点映射到屏幕坐标。若存在旋转、镜像、缩放裁剪，还要把这些变换纳入矩阵组合。
- 追问：前置摄像头镜像时如何修正？
- 评分标准：能说出源/目标坐标系和 Matrix 得 2 分；能考虑旋转镜像裁剪得 3 分。

## 五、并发、协程与响应式流

### Q050 / L2 初中级 / 线程状态

- 面试题：Java 线程的 NEW、RUNNABLE、BLOCKED、WAITING、TIMED_WAITING、TERMINATED 如何切换？
- 考察点：线程状态；锁；wait/join/sleep。
- 参考答案：new 后是 NEW，start 后进入 RUNNABLE，就绪和运行都属于 RUNNABLE；竞争 monitor 锁失败进入 BLOCKED；Object.wait、Thread.join、LockSupport.park 可进入 WAITING；sleep、wait(timeout)、join(timeout) 进入 TIMED_WAITING；run 结束进入 TERMINATED，终止线程不能再次 start。
- 追问：sleep 和 wait 最大区别是什么？
- 评分标准：能列出状态得 1 分；能讲锁释放和唤醒条件得 2 分。

### Q051 / L2 初中级 / Thread 操作

- 面试题：sleep、yield、join、park/unpark 的差异是什么？
- 考察点：CPU 调度；锁释放；阻塞原语。
- 参考答案：sleep 不释放已持有锁，进入超时等待；yield 让出当前时间片但不保证别人执行；join 等待目标线程结束，底层基于 wait；park 不要求持有锁，可被 unpark 或 interrupt 唤醒，是 AQS 等并发工具常用原语。
- 追问：interrupt 对 sleep 中线程会发生什么？
- 评分标准：能说出基本差异得 1 分；能说明 interrupt 与 park/wait/sleep 关系得 2 分。

### Q052 / L3 中高级 / 线程池

- 面试题：ThreadPoolExecutor 七个核心参数和执行策略是什么？
- 考察点：core/max；queue；keepAlive；拒绝策略。
- 参考答案：参数包括 corePoolSize、maximumPoolSize、keepAliveTime、unit、workQueue、ThreadFactory、RejectedExecutionHandler。execute 时通常先用核心线程，再进队列，队列满且未达 max 则创建非核心线程，否则触发拒绝策略。队列类型会强烈影响 max 是否生效。
- 追问：为什么 newCachedThreadPool 在高负载下危险？
- 评分标准：能说出七参数得 1 分；能讲执行顺序和队列影响得 2 分。

### Q053 / L3 中高级 / 锁

- 面试题：synchronized 与 ReentrantLock 的差异是什么？
- 考察点：JVM 锁；AQS；公平锁；中断。
- 参考答案：synchronized 由 JVM 管理，自动释放锁，语法简单；ReentrantLock 基于 AQS，需要 finally 手动 unlock，可选择公平锁，支持 tryLock、lockInterruptibly 和多个 Condition。JDK6 后 synchronized 做了大量优化，性能不再是主要选型理由，更多看能力需求。
- 追问：可重入锁为什么能避免同线程重复获取导致死锁？
- 评分标准：能说出实现层和能力差异得 1 分；能结合 Condition、公平锁、中断选择得 2 分。

### Q054 / L3 中高级 / 死锁

- 面试题：静态锁顺序死锁、动态锁顺序死锁和开放调用分别是什么？
- 考察点：锁顺序；identityHashCode；外部调用。
- 参考答案：静态锁顺序死锁是不同代码路径以不同顺序获取 A/B 锁；统一加锁顺序可解。动态锁顺序死锁是同一方法因参数顺序不同导致锁顺序不同，可用 identityHashCode 决定顺序并用额外锁处理 hash 相等。开放调用指不要持锁调用外部对象方法，避免协作对象互相等待。
- 追问：线上如何通过 jstack 或 traces 识别死锁？
- 评分标准：能说出三类问题得 2 分；能给出工程排查和修复策略得 3 分。

### Q055 / L2 初中级 / ThreadLocal

- 面试题：ThreadLocal 为什么能做到线程隔离？有什么泄漏风险？
- 考察点：ThreadLocalMap；弱引用 key；线程池。
- 参考答案：每个 Thread 内部持有 ThreadLocalMap，key 是 ThreadLocal，value 是该线程自己的副本，所以不同线程互不影响。风险在于线程池线程生命周期很长，value 可能长期持有大对象；key 弱引用被回收后 value 仍可能残留，应在 finally 中 remove。
- 追问：Android Looper 为什么用 ThreadLocal 保存？
- 评分标准：能说出每线程 map 得 1 分；能说明线程池 remove 风险得 2 分。

### Q056 / L2 初中级 / AsyncTask

- 面试题：AsyncTask 内部为什么默认串行？有哪些使用限制？
- 考察点：SerialExecutor；THREAD_POOL_EXECUTOR；Handler。
- 参考答案：AsyncTask 构造 WorkerRunnable 和 FutureTask；execute 默认交给静态 SerialExecutor 排队，再由 THREAD_POOL_EXECUTOR 实际执行；结果通过绑定主 Looper 的 Handler 回调 onPostExecute/onProgressUpdate。一个实例只能执行一次，cancel 只是标记，需要 doInBackground 自己检查。
- 追问：为什么现在更推荐协程、WorkManager 或自定义线程池？
- 评分标准：能说出 SerialExecutor 和 Handler 得 1 分；能说明 cancel/生命周期问题得 2 分。

### Q057 / L2 初中级 / HandlerThread/IntentService

- 面试题：HandlerThread 和 IntentService 的关系是什么？
- 考察点：Looper 线程；串行任务；Service 优先级。
- 参考答案：HandlerThread 是带 Looper 的 Thread，start 后在 run 中 prepare Looper 并 loop，外部可用 getLooper 创建 Handler。IntentService 内部创建 HandlerThread 和 ServiceHandler，onStartCommand 把 Intent 转成消息串行处理，onHandleIntent 在工作线程执行，处理完 stopSelf。
- 追问：IntentService 为什么被废弃？替代方案是什么？
- 评分标准：能说出 HandlerThread Looper 得 1 分；能讲 IntentService 串行和生命周期得 2 分。

### Q058 / L3 中高级 / Kotlin 协程

- 面试题：suspend 函数底层大致如何实现？协程和线程是什么关系？
- 考察点：CPS；状态机；Continuation；调度器。
- 参考答案：suspend 会被编译成带 Continuation 参数的 CPS 形式，函数内部挂起点会变成状态机。协程不是线程，本质是可挂起的计算任务；真正执行仍依赖线程和 Dispatcher。挂起时保存 Continuation，恢复时在指定调度器继续执行。
- 追问：launch 和 async/await 的异常传播有什么差异？
- 评分标准：能说出 Continuation 和状态机得 2 分；能区分协程与线程、调度器得 3 分。

### Q059 / L3 中高级 / 协程作用域

- 面试题：lifecycleScope、viewModelScope 解决什么问题？
- 考察点：结构化并发；生命周期取消。
- 参考答案：lifecycleScope 绑定 LifecycleOwner，生命周期销毁时取消作用域内协程；viewModelScope 绑定 ViewModel，onCleared 时取消。它们减少手动管理 Job 的泄漏风险，但仍需选择合适 Dispatcher，避免主线程执行重任务。
- 追问：repeatOnLifecycle 和 launchWhenStarted 有什么取舍？
- 评分标准：能说出生命周期自动取消得 1 分；能结合结构化并发和 Dispatcher 得 2 分。

### Q060 / L3 中高级 / Flow

- 面试题：冷流、SharedFlow、StateFlow 的差异是什么？
- 考察点：collect 触发；热流缓存；状态/事件。
- 参考答案：普通 Flow 是冷流，collect 时才执行生产者代码，订阅者之间互不共享。SharedFlow 是热流，可配置 replay、额外缓存和溢出策略，适合事件广播。StateFlow 是特殊 SharedFlow，始终有当前 value，适合状态建模，可替代部分 LiveData 场景。
- 追问：为什么 SharedFlow 的 emit 可能挂起？
- 评分标准：能区分冷热流得 1 分；能讲 replay/buffer/状态事件选择得 2 分。

### Q061 / L2 初中级 / Channel

- 面试题：Channel 和 Flow 的关系及选择是什么？
- 考察点：协程通信；背压；API 演进。
- 参考答案：Channel 是协程间通信原语，send/receive 可挂起，也支持缓存，所以并非不支持背压。Flow 是更高层的数据流抽象，官方更推荐用 Flow/SharedFlow/StateFlow 表达 UI 数据和事件。需要明确点对点通信或 actor 模式时 Channel 仍有价值。
- 追问：Channel 关闭后 send/receive 会怎样？
- 评分标准：能说出 send/receive 和背压得 1 分；能结合 Flow 选择得 2 分。

## 六、Jetpack、架构与工程实践

### Q062 / L2 初中级 / LiveData

- 面试题：LiveData observe、setValue、postValue 的核心行为是什么？
- 考察点：LifecycleBoundObserver；版本号；主线程。
- 参考答案：observe 会包装 Observer 并绑定 Lifecycle，DESTROYED 自动移除，STARTED/RESUMED 才活跃。setValue 必须主线程，递增版本并分发；postValue 可子线程调用，写入 pendingData 后切回主线程，短时间多次 post 可能只分发最后一次。
- 追问：为什么 LiveData 有粘性？如何设计非粘性事件？
- 评分标准：能说出生命周期感知和 set/post 差异得 1 分；能解释版本和 post 合并得 2 分。

### Q063 / L2 初中级 / ViewModel

- 面试题：ViewModel 如何在配置变更中存活？什么时候清理？
- 考察点：ViewModelStore；NonConfigurationInstance；Factory。
- 参考答案：ComponentActivity 持有 ViewModelStore，配置变更时通过 NonConfigurationInstance 保留 Store，新 Activity 重新拿到同一 ViewModel。只有真正 finish 或宿主销毁时，ViewModelStore.clear 触发 ViewModel.onCleared。ViewModelProvider 通过 key 和 Factory 创建或复用实例。
- 追问：ViewModel 能持有 Activity Context 吗？
- 评分标准：能说出 Store 保留得 1 分；能讲 Factory/key/onCleared 得 2 分。

### Q064 / L3 中高级 / MVC/MVP/MVVM/MVI

- 面试题：MVC、MVP、MVVM、MVI 的核心差异和 Android 落地风险是什么？
- 考察点：职责分离；状态管理；单向数据流。
- 参考答案：MVC 容易让 Activity/Fragment 变胖；MVP 用 Presenter 承担逻辑并通过 View 接口交互，可测试但接口膨胀；MVVM 用 ViewModel 暴露状态，View 观察数据，适合 Jetpack；MVI 强调 Intent -> Reducer -> State 的单向流，更利于复杂状态一致性，但样板和学习成本更高。
- 追问：什么时候不该强行上 MVI？
- 评分标准：能区分职责得 1 分；能结合复杂状态、测试和成本取舍得 2 分。

### Q065 / L2 初中级 / 设计模式

- 面试题：单例、工厂、构建者、代理、策略在 Android 中各适合什么场景？
- 考察点：常见模式；场景映射。
- 参考答案：单例适合全局无状态或有严格生命周期的服务；工厂隐藏创建细节并支持传参选择实现；Builder 适合参数多且可选的对象；代理用于 Hook、懒加载、权限控制、AOP；策略把可变算法封装成可替换实现，例如图片加载、埋点上报或排序。
- 追问：过度使用模式会带来什么问题？
- 评分标准：能说出模式定义得 1 分；能贴近 Android 场景得 2 分。

### Q066 / L3 中高级 / APT

- 面试题：运行时注解和编译时注解如何取舍？APT 工程如何组织？
- 考察点：Retention；annotationProcessor/kapt；生成代码。
- 参考答案：运行时注解需要 Retention.RUNTIME，可通过反射读取，灵活但有运行时开销。编译时注解在编译期扫描元素并生成代码，适合路由、依赖注入、初始化注册等。工程上通常拆成 annotation 模块、processor 模块、runtime 模块，App implementation 注解/运行时库，用 kapt 或 annotationProcessor 引入处理器。
- 追问：为什么注解和处理器不建议放同一 module？
- 评分标准：能说出 Retention 和反射/APT 差异得 1 分；能讲模块拆分和 kapt 得 2 分。

### Q067 / L3 中高级 / ArchUnit

- 面试题：如何用 ArchUnit 防止大型工程架构腐化？
- 考察点：字节码分析；依赖规则；CI。
- 参考答案：ArchUnit 基于字节码模型分析包、类、字段、方法依赖，可定义分层依赖、禁止循环依赖、包位置约束、继承约束等规则。在 CI 中执行规则可以阻止新增违规依赖，比人工 code review 更稳定。规则要从高价值边界开始，避免一次性规则过多导致落地失败。
- 追问：如果本地和 CI 扫描结果不一致，如何排查？
- 评分标准：能说出字节码分析和规则类型得 1 分；能结合 CI 和渐进落地得 2 分。

### Q068 / L4 高级/资深 / 解耦重构

- 面试题：大型 Android 工程中如何做渐进式解耦？
- 考察点：接口隔离；组合替代继承；胶水层；工具。
- 参考答案：先识别高耦合点：数据类携带业务方法、继承只为复用方法、跨层直接依赖、路由无法传参等。处理方式包括把数据类方法抽成扩展/工具，继承改组合或委托，抽接口依赖抽象，引入胶水层做模型转换，用工厂接口解决创建参数问题。配合 IDE 重构工具和 ArchUnit 防回流。
- 追问：如何保证重构不破坏行为？
- 评分标准：能给出解耦手段得 2 分；能说明渐进推进、验证和防腐机制得 3 分。

### Q069 / L3 中高级 / 分层架构

- 面试题：为什么大项目初期可能只分 biz/base 两层？后续如何演进？
- 考察点：架构落地；复杂度控制；胶水层。
- 参考答案：在耦合严重的大项目里，过细分层会导致改造面过大，先用 biz/base 两层降低推进难度是务实选择。但缺点是业务层和基础层仍可能互相污染，后续可引入胶水层隔离模型转换和适配逻辑，并在业务层内部逐步细分 MVVM、domain/data 等。
- 追问：什么时候分层会变成过度设计？
- 评分标准：能说出务实分层理由得 1 分；能讲演进和防腐得 2 分。

### Q070 / L3 中高级 / TDD/单测

- 面试题：TDD 的适用场景、价值和 Android 单测三部曲是什么？
- 考察点：测试驱动；可测性；GIVEN/WHEN/THEN。
- 参考答案：TDD 是先写失败用例，再实现最小可运行代码，再重构。适合新项目或相对独立的纯业务逻辑；历史包袱重、强 UI/强框架依赖场景很难纯 TDD。单测三部曲是 GIVEN 准备环境，WHEN 执行被测行为，THEN 断言结果。Mockito/MockK 可用，但大量 mock 往往说明设计可测性不足。
- 追问：如何把不可测代码改到可测？
- 评分标准：能说出 TDD 流程和三部曲得 1 分；能讨论适用边界和重构可测性得 2 分。

### Q071 / L4 高级/资深 / 启动初始化

- 面试题：如何设计支持多进程、依赖链和线程调度的初始化框架？
- 考察点：APT；依赖图；环检测；进程过滤。
- 参考答案：用注解声明初始化器依赖、线程模式、支持进程；APT 在编译期收集信息生成 ComponentInfo 和 Registry，构建主线程链和工作线程链。运行时按当前进程过滤初始化器，主线程链串行执行，工作线程链可并行；构建依赖链时记录构建中和已构建节点，发现构建中节点再次出现即循环依赖。初始化入口可放 attachBaseContext，避免 ContentProvider 多进程限制。
- 追问：某个初始化器既被主线程依赖又想放后台，如何处理？
- 评分标准：能说出注解+APT+依赖图得 2 分；能讲进程过滤、线程策略和环检测得 3 分。

### Q072 / L3 中高级 / 换肤架构

- 面试题：动态换肤系统如何设计？静态 XML View 和动态 View 分别怎么处理？
- 考察点：token；LayoutInflater.Factory；外部 Resources。
- 参考答案：统一给颜色/图片定义 token，日夜间或皮肤包中同 token 对应不同资源。动态 View 通过 getColor/getDrawable(token) 获取；XML 静态 View 可在 Activity super.onCreate 前设置 LayoutInflater.Factory，创建 View 时拦截特定前缀资源并替换。皮肤包可打成 APK，通过 PackageManager 解析未安装 APK 并构造 Resources。
- 追问：AppCompatActivity 下 Factory 如何兼容 AppCompatDelegate？
- 评分标准：能说出 token 和 Factory 得 2 分；能讲资源包加载和 AppCompat 兼容得 3 分。

### Q073 / L3 中高级 / 工程效率

- 面试题：如何提高皮肤包脚本和资源映射效率？
- 考察点：脚本 IO；编译期映射；Transform/ASM。
- 参考答案：脚本层面应减少慢速逐文件 Python 解析，使用更高效的字符串匹配、批量文件拷贝和增量处理。运行时 token 到资源 id 若依赖 Resources.getIdentifier 会慢，可在编译期扫描 R 信息生成 token-id 映射，运行时直接查表。若需要处理 class，可用 Transform 配合 ASM/Javassist。
- 追问：如何验证脚本提速不是牺牲正确性？
- 评分标准：能说出 getIdentifier 慢和编译期映射得 1 分；能讨论增量、缓存和校验得 2 分。

## 七、性能、稳定性、异常治理

### Q074 / L3 中高级 / ANR

- 面试题：ANR 的常见超时类型、原因和分析步骤是什么？
- 考察点：Input/Broadcast/Service/Provider；traces；主线程。
- 参考答案：常见阈值包括输入事件约 5s、前台广播约 10s、后台广播约 60s、前台 Service 约 20s、后台 Service 约 200s、Provider 约 10s。原因包括主线程 IO/CPU 密集、锁等待、死锁、同步 Binder 等。分析看 logcat、traces 主线程栈、CPU/IO/内存、Binder 调用链和业务时间线。
- 追问：如果主线程栈是 Binder transact，下一步看什么？
- 评分标准：能列出类型和常见原因得 1 分；能讲系统化分析链路得 2 分。

### Q075 / L3 中高级 / OOM

- 面试题：Android OOM 的治理思路是什么？
- 考察点：内存上限；泄漏；图片；线程。
- 参考答案：OOM 本质是进程已用内存加申请内存超过限制。治理包括减少对象泄漏、控制图片尺寸和格式、按屏幕尺寸采样、限制缓存、减少预加载、控制线程数量、及时释放大对象、必要时使用 64 位或大内存策略。还要用 heap dump 区分泄漏和瞬时峰值。
- 追问：为什么线程过多也会导致 OOM？
- 评分标准：能说出内存上限和泄漏/图片得 1 分；能区分泄漏与峰值并给治理策略得 2 分。

### Q076 / L3 中高级 / 异常捕获

- 面试题：Thread.setDefaultUncaughtExceptionHandler 在 Android 中如何影响进程？
- 考察点：Java 线程异常；Android KillApplicationHandler。
- 参考答案：Java 普通子线程未捕获异常理论上只终止该线程；但 Android Runtime 在线程未捕获异常后会走系统异常处理链，最终 KillApplicationHandler 通常会杀掉进程，所以主线程和子线程未捕获异常都会导致应用崩溃。业务可设置默认 handler 做日志落盘，但不应吞掉异常后继续不一致状态。
- 追问：Crash 兜底里做 IO 有什么风险？
- 评分标准：能说出 Android 子线程异常也会杀进程得 1 分；能说明兜底记录和状态风险得 2 分。

### Q077 / L2 初中级 / StrictMode

- 面试题：StrictMode 能检测哪些问题？怎么开启？
- 考察点：ThreadPolicy；VmPolicy；Penalty。
- 参考答案：StrictMode 可按线程策略检测磁盘读写、网络、自定义慢调用；按 VM 策略检测 Activity、Closable、SQLite 等对象泄漏和实例数。通常在 debug Application 中 setThreadPolicy/setVmPolicy，并配置 penaltyLog、penaltyDeath、闪红框等。
- 追问：为什么线上不建议直接 penaltyDeath？
- 评分标准：能说出策略和惩罚得 1 分；能结合 debug/线上策略得 2 分。

### Q078 / L2 初中级 / 布局性能

- 面试题：布局优化有哪些常见方向？
- 考察点：层级；懒加载；异步；过度绘制。
- 参考答案：减少层级和不必要嵌套，使用 ConstraintLayout/merge/include 合理组织；低频 UI 用 ViewStub 懒加载；复杂布局可考虑 AsyncLayoutInflater；减少 overdraw，避免主线程重 IO 和构造耗时；RecyclerView 用 DiffUtil、payload、缓存策略减少 bind 成本。
- 追问：如何用工具发现布局卡顿？
- 评分标准：能列出常见手段得 1 分；能结合工具和具体场景得 2 分。

### Q079 / L3 中高级 / 卡顿/FPS

- 面试题：线上卡顿问题如何从 FPS 监控走到根因定位？
- 考察点：帧率；长帧；Trace；主线程。
- 参考答案：FPS 只能发现现象，要进一步记录长帧时间点、页面、操作路径和主线程任务。复现后用 Perfetto/System Trace/Method Trace 看主线程、RenderThread、Binder、锁、IO 和 Choreographer traversal。结合业务埋点缩小范围，最后用小步实验验证修复。
- 追问：Jank 是 CPU 问题还是 GPU 问题如何区分？
- 评分标准：能说出 FPS 不等于根因得 1 分；能给出 trace 和业务定位闭环得 2 分。

### Q080 / L3 中高级 / 局部性

- 面试题：局部性原理如何指导移动端性能优化？
- 考察点：时间局部性；空间局部性；缓存层级。
- 参考答案：时间局部性指近期访问的数据可能再次访问，空间局部性指相邻地址可能被访问。移动端可据此优化数据结构和访问模式：顺序访问数组通常比链表更缓存友好；批量处理减少随机 IO；热点配置缓存到内存；图片和资源按页面生命周期预取但控制大小。
- 追问：为什么 SparseArray 的数组结构对小数据量友好？
- 评分标准：能解释两种局部性得 1 分；能结合 Android 数据/IO/缓存得 2 分。

### Q081 / L3 中高级 / 疑难 bug

- 面试题：讲一个疑难 bug，面试官希望听到什么结构？
- 考察点：问题定义；证据链；假设验证；复盘。
- 参考答案：不要只讲“最后改了哪里”。应按现象和影响、可观测证据、排查路径、关键假设、验证实验、修复方案、上线风险控制、复盘沉淀组织。比如脏数据问题可从埋点、堆栈、日志、录屏、用户回访串证据链，而不是凭经验猜。
- 追问：如果无法本地复现，如何推进？
- 评分标准：能说清结构得 1 分；能体现证据驱动和复盘机制得 2 分。

### Q082 / L4 高级/资深 / 稳定性体系

- 面试题：如何建立 Android 稳定性治理闭环？
- 考察点：监控；归因；灰度；回滚；自动化。
- 参考答案：闭环包括 Crash/ANR/OOM/卡顿/启动/耗电指标采集，按版本、机型、系统、页面、业务聚合归因；灰度发布和阈值拦截；问题自动分派；高风险功能开关和回滚；复盘后补充单测、集成测试、ArchUnit/静态扫描或运行时监控。
- 追问：如何避免指标好看但用户体验变差？
- 评分标准：能列出监控和发布闭环得 2 分；能讲防回归机制得 3 分。

## 八、网络、安全与计算机基础

### Q083 / L1 实习/校招 / 网络分层

- 面试题：五层网络模型每层职责是什么？HTTP 属于哪层？
- 考察点：应用层；传输层；网络层；链路层；物理层。
- 参考答案：应用层定义应用协议，如 HTTP、DNS；传输层提供端到端传输，如 TCP/UDP；网络层负责寻址路由，如 IP；链路层负责相邻节点帧传输；物理层传输比特流。HTTP 属于应用层，通常基于 TCP/TLS 或 QUIC。
- 追问：DNS 解析发生在请求链路的哪个阶段？
- 评分标准：能说出五层职责得 1 分；能结合 HTTP/TCP/IP 得 2 分。

### Q084 / L2 初中级 / TCP/UDP

- 面试题：TCP 和 UDP 的差异是什么？移动端如何选择？
- 考察点：连接；可靠性；拥塞控制；实时性。
- 参考答案：TCP 面向连接，提供可靠、有序、拥塞控制和重传，适合大多数业务请求；UDP 无连接，开销低但不保证可靠和顺序，适合实时音视频、游戏、QUIC 等由上层处理可靠性的场景。移动端还要考虑弱网、重连、耗电和网络切换。
- 追问：HTTP/3 为什么基于 QUIC/UDP？
- 评分标准：能说出可靠性和连接差异得 1 分；能结合移动弱网选择得 2 分。

### Q085 / L2 初中级 / TCP 握手挥手

- 面试题：为什么 TCP 建连是三次握手，断连通常是四次挥手？
- 考察点：全双工；序列号同步；半关闭。
- 参考答案：三次握手用于双方确认收发能力和初始序列号：客户端 SYN，服务端 SYN+ACK，客户端 ACK。断连是全双工半关闭，主动方 FIN 后对端先 ACK，等对端数据发送完再 FIN，主动方 ACK，所以通常四次。TIME_WAIT 用于处理迟到报文和确保最后 ACK 可重传。
- 追问：为什么不是两次握手？
- 评分标准：能说出三次握手过程得 1 分；能解释四次挥手和 TIME_WAIT 得 2 分。

### Q086 / L3 中高级 / HTTP 版本

- 面试题：HTTP/1.1、HTTP/2、HTTP/3 的关键差异是什么？
- 考察点：连接复用；队头阻塞；QUIC。
- 参考答案：HTTP/1.1 支持持久连接但并发能力有限，存在应用层队头阻塞。HTTP/2 基于一个 TCP 连接多路复用、头部压缩、二进制帧，但仍受 TCP 层队头阻塞影响。HTTP/3 基于 QUIC/UDP，把连接迁移、拥塞控制、加密和多路复用放到 QUIC，改善弱网和丢包场景。
- 追问：HTTP/2 多路复用为什么仍可能被 TCP 队头阻塞影响？
- 评分标准：能说出三版差异得 2 分；能解释 TCP 与 QUIC 队头阻塞得 3 分。

### Q087 / L3 中高级 / HTTPS

- 面试题：HTTPS 如何同时解决加密、完整性和身份认证？
- 考察点：TLS；证书；CA；混合加密。
- 参考答案：HTTPS 基于 TLS。服务端证书由 CA 签名，客户端验证证书链和域名来认证身份；握手阶段用非对称加密/密钥交换协商会话密钥；数据阶段用对称加密提高性能；消息认证码或 AEAD 保证完整性。证书被篡改会导致签名校验失败。
- 追问：为什么不全程使用非对称加密？
- 评分标准：能说出证书、对称/非对称混合得 2 分；能解释完整性和证书链得 3 分。

### Q088 / L2 初中级 / 加密算法

- 面试题：对称加密、非对称加密、摘要、Base64 分别是什么？
- 考察点：AES/DES；RSA；MD5/SHA；编码。
- 参考答案：对称加密加解密用同一密钥，如 AES，速度快但密钥分发难；非对称加密用公钥/私钥，如 RSA，适合密钥交换和签名但较慢；摘要算法如 MD5/SHA 单向，不是加密；Base64 是编码，不提供安全性。
- 追问：签名和加密的方向有什么不同？
- 评分标准：能区分四类概念得 1 分；能结合 HTTPS 使用方式得 2 分。

### Q089 / L2 初中级 / IPC

- 面试题：Linux/Android 常见 IPC 方式有哪些？Binder 与 Messenger 怎么选？
- 考察点：管道；共享内存；Socket；Binder；Messenger。
- 参考答案：Linux IPC 包括管道/FIFO、信号、信号量/互斥、共享内存、Socket、消息队列等。Android 常见有 Binder、Messenger、AIDL、ContentProvider、Broadcast、Socket、文件等。Messenger 基于 Handler 串行处理，适合简单消息；AIDL/Binder 更适合复杂接口和高并发。
- 追问：SharedMemory/Ashmem 适合传什么？
- 评分标准：能列出 IPC 方式得 1 分；能按复杂度选择 Messenger/AIDL 得 2 分。

### Q090 / L3 中高级 / Zygote/fork

- 面试题：Android 为什么用 Zygote fork 应用进程？
- 考察点：预加载；写时复制；启动性能。
- 参考答案：Zygote 预加载常用类和资源，应用启动时由 system_server 请求 Zygote fork，新进程继承已加载内容，配合写时复制降低启动成本和内存占用。fork 后子进程进入 ActivityThread.main，建立主线程消息循环。
- 追问：fork 后父子进程变量是什么关系？
- 评分标准：能说出预加载和 COW 得 1 分；能联系应用启动链路得 2 分。

### Q091 / L3 中高级 / Cookie/Session/Token

- 面试题：HTTP 无状态下如何做登录态？Cookie、Session、Token 的取舍是什么？
- 考察点：状态维护；安全；移动端。
- 参考答案：HTTP 无状态，服务端可用 Cookie 携带 session id，再在服务端查 session；移动端也常用 token 放在 header，由服务端验证签名或查存储。Cookie 自动携带但要防 CSRF、Secure、HttpOnly；token 更适合多端和 API，但要注意存储安全、过期刷新和吊销。
- 追问：Android 端 token 存 SharedPreferences 安全吗？
- 评分标准：能说出无状态和三者关系得 1 分；能讨论安全存储和过期策略得 2 分。

## 九、项目场景题

### Q092 / L4 高级/资深 / 架构治理

- 面试题：如果接手一个耦合严重的千万级 Android 工程，你的前 3 个月治理路线是什么？
- 考察点：盘点；边界；自动化；灰度。
- 参考答案：第一阶段盘点依赖图、业务域、构建耗时、稳定性 Top 问题；第二阶段选高收益边界做最小规则，如 biz 不反向依赖 base、禁止新增循环依赖；第三阶段用 ArchUnit/CI 防新增腐化，同时选择一个低风险业务试点解耦。过程中保持兼容层和灰度验证，避免大爆炸重构。
- 追问：如何向业务证明治理收益？
- 评分标准：能提出分阶段路线得 2 分；能说明指标、自动化和风险控制得 3 分。

### Q093 / L4 高级/资深 / 启动优化

- 面试题：如何优化多进程 App 的启动初始化耗时？
- 考察点：初始化分级；进程过滤；依赖图；异步。
- 参考答案：先通过 trace 和埋点识别冷启动关键路径，把初始化分为必须同步、可延迟、可后台、按进程需要。用注解/APT 或配置生成依赖图，按当前进程过滤组件，主线程只执行必要链路，后台链路并行但遵守依赖。避免 ContentProvider 隐式初始化过多，监控初始化耗时和失败降级。
- 追问：如何处理后台初始化依赖主线程结果？
- 评分标准：能说出分类和测量得 2 分；能讲进程过滤、依赖链、降级得 3 分。

### Q094 / L3 中高级 / 列表性能

- 面试题：一个复杂信息流滑动卡顿，你如何排查和优化？
- 考察点：RecyclerView；bind；图片；主线程；预取。
- 参考答案：先用 FPS/trace 定位卡顿发生在布局、bind、图片解码、网络回调还是 GC。优化包括简化 item 布局、使用 payload 局部刷新、DiffUtil、稳定 id、控制嵌套 RecyclerView、图片预加载和尺寸采样、避免 onBind 做重计算、合理调整缓存池和预取。
- 追问：如何避免优化后出现错位或脏数据？
- 评分标准：能列出排查方向得 1 分；能给出 RecyclerView 针对性策略和验证得 2 分。

### Q095 / L4 高级/资深 / 动态化/插件化

- 面试题：如果要给 App 做插件化能力，你会如何评估风险？
- 考察点：兼容性；安全；资源；生命周期；灰度。
- 参考答案：先明确目标是动态发布、业务隔离还是包体治理。风险包括 Android 版本私有 API 限制、ClassLoader 冲突、资源 id 冲突、四大组件生命周期、签名校验、安全边界、崩溃归因、热更新回滚。工程上要灰度、开关、插件签名校验、版本协议和充分兼容测试。
- 追问：什么时候不应该使用插件化？
- 评分标准：能列出核心风险得 2 分；能结合目标、灰度和安全策略得 3 分。

### Q096 / L3 中高级 / 跨进程数据一致性

- 面试题：多进程 App 中配置数据如何保证一致性？为什么不用 SharedPreferences？
- 考察点：IPC；缓存；一致性；失败恢复。
- 参考答案：SP 非进程安全，频繁跨进程写可能丢数据。可选单进程 owner + Binder/ContentProvider 对外提供读写；或用数据库/WAL 并加事务；热点配置用内存缓存加版本号和变更通知。需要定义一致性级别、失败重试和冷启动加载策略。
- 追问：ContentProvider 的并发线程安全如何保证？
- 评分标准：能指出 SP 风险得 1 分；能给出 owner/DB/通知方案得 2 分。

### Q097 / L3 中高级 / 扫码功能

- 面试题：基于 CameraX 做扫码功能，如何设计模块和处理坐标问题？
- 考察点：CameraX；ImageAnalysis；解码；矩阵。
- 参考答案：模块上拆成相机预览、帧分析、解码器适配、结果渲染、生命周期绑定。Preview 负责展示，ImageAnalysis 输出帧给扫码 SDK，识别结果顶点通过 Matrix 从裁剪图坐标映射到 PreviewView 坐标。要处理旋转、镜像、节流、背压策略和生命周期释放。
- 追问：如何避免帧分析阻塞预览？
- 评分标准：能说出 CameraX 三块能力得 1 分；能讲坐标矩阵和背压得 2 分。

### Q098 / L4 高级/资深 / 换肤效率

- 面试题：一个 token 换肤方案上线后卡顿明显，你如何优化？
- 考察点：资源查找；缓存；编译期生成；Factory。
- 参考答案：先确认卡顿点是否在 getIdentifier、inflate 拦截、资源包加载或全量刷新。优化包括编译期生成 token 到 id 的映射，运行时查表；资源对象缓存；只替换可见区域；对 XML 静态 View 在 Factory 阶段记录可换肤属性；皮肤切换时按页面/生命周期分批刷新。
- 追问：如何保证新增资源不会漏映射？
- 评分标准：能定位 getIdentifier 和刷新成本得 1 分；能提出编译期映射、缓存和增量刷新得 2 分。

### Q099 / L3 中高级 / 单测落地

- 面试题：团队单测落地阻力大，如何推进？
- 考察点：可测性；ROI；模板；CI。
- 参考答案：从高价值纯逻辑模块和历史 bug 回归用例开始，不要求全量覆盖。建立 GIVEN/WHEN/THEN 模板、测试命名规范、Mock 使用边界，推动业务逻辑从 Android Framework 依赖中抽离。CI 只拦截新增核心规则，覆盖率作为趋势指标而非单一 KPI。
- 追问：如何处理旧代码强依赖静态单例？
- 评分标准：能给出渐进策略得 1 分；能结合可测性重构和 CI 得 2 分。

### Q100 / L4 高级/资深 / ANR 线上治理

- 面试题：线上 ANR Top 1 是偶现锁等待，如何推进？
- 考察点：证据采集；锁图；降级；修复验证。
- 参考答案：先聚合 traces，确认主线程等待的锁对象和持锁线程；补充锁等待埋点或 trace section，关联页面、机型、线程池任务和 Binder 调用。短期可降低锁粒度、超时降级或异步化；长期拆分共享状态、统一锁顺序、避免持锁外部调用。上线后看 ANR 指标和长尾。
- 追问：如果 traces 只有 nativePollOnce，说明什么？
- 评分标准：能讲锁等待定位得 2 分；能提出短期止血和长期治理得 3 分。

## 十、算法与编码题

### Q101 / L1 实习/校招 / 二叉树遍历

- 面试题：写出二叉树 BFS、前序、中序、后序遍历的思路。
- 考察点：递归；队列；遍历顺序。
- 参考答案：BFS 使用队列，先入根节点，循环 poll 后依次加入左右子节点。DFS 前序是根左右，中序是左根右，后序是左右根，可递归实现，也可用栈迭代实现。
- 追问：如何按层输出每一层节点？
- 评分标准：能说出顺序和队列/递归得 1 分；能扩展层序得 2 分。

### Q102 / L2 初中级 / 快速排序

- 面试题：快速排序 partition 的核心是什么？平均和最坏复杂度是多少？
- 考察点：分治；pivot；原地交换。
- 参考答案：选择 pivot，把小于 pivot 的元素放左边，大于的放右边，partition 返回 pivot 最终位置，然后递归左右区间。平均 O(nlogn)，最坏 O(n^2)，可通过随机 pivot、三数取中、尾递归优化降低风险。
- 追问：快排稳定吗？为什么？
- 评分标准：能写出 partition 思路得 1 分；能讲复杂度和退化原因得 2 分。

### Q103 / L2 初中级 / 快慢指针

- 面试题：如何删除链表倒数第 k 个节点？
- 考察点：双指针；dummy；边界。
- 参考答案：使用 dummy 指向 head，first 先走 k 步，然后 first 和 second 同时走，直到 first 到尾；second.next 就是待删节点，修改 second.next。dummy 能统一删除头节点的边界。
- 追问：k 等于链表长度时如何处理？
- 评分标准：能说出双指针间隔 k 得 1 分；能处理头节点和非法 k 得 2 分。

### Q104 / L1 实习/校招 / 合并有序数组

- 面试题：如何原地合并两个有序数组到 nums1？
- 考察点：双指针；从后往前；空间优化。
- 参考答案：nums1 后半部分有空位，从 nums1 有效尾 p1、nums2 尾 p2、总尾 tail 开始，每次把较大值放到 tail 并左移。这样不会覆盖 nums1 尚未比较的元素，时间 O(m+n)，额外空间 O(1)。
- 追问：如果从前往后合并会遇到什么问题？
- 评分标准：能说出从后往前得 1 分；能说明不覆盖原因得 2 分。

### Q105 / L1 实习/校招 / 合并有序链表

- 面试题：如何合并两个升序链表？
- 考察点：dummy；双指针；链表操作。
- 参考答案：创建 dummy 和当前指针 cur，比较 l1/l2 当前节点，把较小节点接到 cur 后面并移动对应指针，循环结束后接上剩余链表，返回 dummy.next。
- 追问：递归写法的栈风险是什么？
- 评分标准：能写出 dummy 双指针得 1 分；能说明空间和边界得 2 分。

### Q106 / L2 初中级 / Top K

- 面试题：数组第 k 大元素有哪些解法？如何达到期望 O(n)？
- 考察点：堆；快速选择；复杂度。
- 参考答案：可用大小为 k 的小顶堆维护当前前 k 大，时间 O(nlogk)。也可用快速选择，partition 后只递归包含第 k 大的半边，平均 O(n)，最坏 O(n^2)，随机 pivot 可降低退化概率。
- 追问：海量数据无法全放内存时怎么做？
- 评分标准：能说出堆和快选得 1 分；能讲复杂度和海量扩展得 2 分。

### Q107 / L2 初中级 / 大数相加

- 面试题：两个逆序链表表示数字，如何相加？
- 考察点：进位；链表；递归/迭代。
- 参考答案：从两个链表头开始逐位相加，加上 carry，当前节点值为 sum%10，下一轮 carry=sum/10。循环直到两个链表都为空且 carry 为 0。非十进制只需替换进制基数。
- 追问：如果链表是正序存储怎么办？
- 评分标准：能说出逐位进位得 1 分；能处理尾部 carry 和不同长度得 2 分。

### Q108 / L3 中高级 / 局部反转链表

- 面试题：如何一次遍历反转链表 [left,right] 区间？
- 考察点：头插法；dummy；指针安全。
- 参考答案：使用 dummy，pre 走到 left 前一个节点，cur 指向 left。循环 right-left 次，把 cur.next 摘下插到 pre.next 前面：next=cur.next，cur.next=next.next，next.next=pre.next，pre.next=next。返回 dummy.next。
- 追问：为什么需要 dummy？如何避免断链？
- 评分标准：能说出头插法步骤得 2 分；能画清指针变化和边界得 3 分。

### Q109 / L3 中高级 / 字符串匹配

- 面试题：KMP 解决了什么问题？next 数组表达什么？
- 考察点：模式串；最长相等前后缀；回退。
- 参考答案：KMP 在文本匹配失败时，不回退文本指针，而根据模式串 next 数组决定模式串回退位置。next 表示当前位置之前子串的最长相等前后缀长度，从而复用已经比较过的信息，整体时间 O(n+m)。
- 追问：next 数组如何手算？
- 评分标准：能说出不回退文本指针得 1 分；能解释最长前后缀得 2 分。

## 未读取或受限来源

- 部分掘金、CSDN、个人博客、腾讯文档、企业内网页在外部抓取时可能受登录、反爬、站点空壳或权限限制；已保留原链接并以 Notion 中可读内容为主生成题目。
- 外部文章只用于理解和归纳，不在本文档复制全文。

## 面试使用建议

- L1/L2 适合作为基础筛选，重点看候选人是否能准确表达概念并写出边界条件。
- L3 适合 3 年以上或核心业务候选人，重点看机制链路、排查方法和工程取舍。
- L4 适合高级/资深候选人，重点看架构判断、稳定性闭环、复杂项目推进和风险控制。