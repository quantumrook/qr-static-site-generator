---
title: "Example"
created: "2025-01-07"
modified: 
    - "2025-01-07"
    - "2025-01-08"
---

## Table of Features Implemented

| Feature | Implemented |
| ------- | ----------- |
| Unordered Lists | Yes |
| Ordered Lists | Yes |
| Task Lists | Yes |
| images, internal | Yes |
| images, external | Yes |
| links, internal | Yes |
| links, external | Yes |
| links, embedded | No |
| Tables | Yes |
| Callouts | Yes |
| Code Blocks | Yes |
| Math | No |

![small banner](/content/small_banner.png)

## This is H2

Here's **some text**.

I should **probably** get *some* ***lorem-ipsum*** in here.

~~TODO: add lorem-ipsum~~

Here's an [internal link](#this-is-h2) to the same file. And here's an [internal site](/Example2.md) link. Here's a [link](/Example2.md#other-h2) to a header in the other file.

Now for the tricky part (?) let's link to the formatting [sheet](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax). And now an external image: ![Engelbart](https://history-computer.com/ModernComputer/Basis/images/Engelbart.jpg)

### Lorem Ipsum

> [!note] 
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ullamcorper eros at maximus porta. Vestibulum lectus metus, ornare nec suscipit at, sagittis vitae augue. Vestibulum sem velit, lobortis eu mattis nec, pulvinar ac metus. Nulla ex quam, gravida in efficitur vel, accumsan vitae lorem. In at malesuada mauris. Etiam id dui sit amet nisl efficitur fermentum. Nam mattis sapien eget dolor imperdiet suscipit. Phasellus tristique eleifend dolor nec ultrices. Fusce semper ex mollis risus vehicula fringilla. Vivamus commodo ut tortor vitae ultricies. Mauris consequat fermentum egestas. Nunc pulvinar mauris ipsum, a ornare massa consectetur eget.

Donec venenatis rhoncus porttitor. Aliquam sed luctus mi. Fusce vel massa vel magna luctus sollicitudin ut vitae magna. Donec pulvinar consequat nisi, convallis elementum metus condimentum id. Mauris gravida eros non odio varius ornare. Mauris vel orci tincidunt, lobortis augue nec, ultrices lacus. Etiam feugiat sagittis rutrum. Fusce in sapien aliquam, pellentesque risus eu, iaculis est. Nam convallis, mi eget maximus sagittis, justo nisi elementum ex, ut luctus risus mi eu ipsum. Aliquam sit amet egestas diam. Donec non massa ac turpis tempus suscipit.

> Etiam ultricies massa et placerat placerat. Sed tempus nec metus vel ullamcorper. Vestibulum tempus id mauris in eleifend. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris suscipit tincidunt tellus, in auctor eros laoreet et. Vivamus nisl ligula, facilisis non interdum accumsan, dapibus vel augue. Ut aliquam ligula a dolor lobortis pellentesque. Vivamus nec neque volutpat massa dignissim aliquam sed nec nibh. Nullam vitae ullamcorper est. Morbi condimentum dolor non nisl hendrerit fringilla.
> 
> Quisque tempus ipsum eros, non vulputate mauris venenatis eu. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vehicula magna sit amet leo fringilla, non pellentesque ante porta. Integer semper dapibus augue nec accumsan. Duis felis turpis, auctor sit amet lacinia et, tincidunt ac mi. Donec elementum mauris et dictum suscipit. Duis pellentesque augue lectus. Praesent gravida molestie interdum. Vivamus scelerisque erat vel diam efficitur, sit amet mollis urna dapibus. Proin sed fringilla est. Nulla ultricies nisl ut orci eleifend semper. Aliquam eu nulla ligula. Mauris nec fringilla odio. Sed vestibulum purus ut imperdiet rutrum.

Curabitur vitae lacus commodo, suscipit dolor tincidunt, tempor orci. Morbi quis erat ligula. Sed arcu eros, sodales ac urna eget, facilisis lobortis tortor. Morbi felis metus, tincidunt eu gravida et, scelerisque dapibus augue. Fusce aliquam condimentum euismod. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas nec porta mi. Curabitur est magna, ultricies non congue id, condimentum sit amet magna. Aenean sagittis purus massa, condimentum gravida lorem auctor eget. 

---

### Lists

Let's see what we're working on for v0.02:

- task lists
- unordered lists
	- sub lists
- ordered lists
- use python 3.

#### But in order:

1. unordered lists
	1. sub lists
2. ordered lists
3. task lists

And now let's track our progress:

- [x] unordered lists
	- [x] sub lists
- [x] ordered lists
- [ ] task lists

## Now onto some code

Here, we create a simple loop in python:

```python
#before: start, stop, step
for i in range(start, stop, step):
    f.integrate(i)
```

Now let's step through this:

```
define start
define stop
define our step size
do numerical integration
```
