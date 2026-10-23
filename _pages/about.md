---
layout: about
title: about
permalink: /
subtitle: Head of Knowit Research · Part-time Lecturer in Software Engineering, University of Oslo

profile:
  align: right
  image: profile.jpg
  image_circular: true # crops the image to make it circular
  more_info: >
    <img class="profile-sidekick" src="/assets/img/octocat.png" alt="Octocat version of Jan Henrik" width="264" height="388">
    <p>Knowit, Oslo</p>
    <p>Department of Informatics, <span style="white-space: nowrap">University of Oslo</span></p>

selected_papers: false # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: false # no news items on this site

latest_posts:
  enabled: false # no blog on this site
---

<style>
  /* Octocat standing in front of the lower-left edge of the profile photo.
     margin-top is a % of the profile width, so the cat (38% wide, 264x388) ends ~10% below the circle. */
  .profile { position: relative; }
  .profile .rounded-circle { border: 4px solid var(--global-bg-color, #fff); }
  .profile-sidekick {
    position: absolute; top: 0; left: -5%; margin-top: 54%;
    width: 38% !important; height: auto !important; /* the theme forces .profile img to full width */
    filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.25));
    transition: transform 0.25s ease; transform-origin: bottom center;
  }
  .profile:hover .profile-sidekick { transform: rotate(-6deg) translateY(-4px); }
  .profile .more-info { margin-top: 2rem; }
  /* On phones the theme makes the profile full width; keep it a compact, centred block instead.
     The sidekick is positioned in % of .profile, so it shrinks along with the photo. */
  @media (max-width: 575.98px) {
    .profile.float-right { float: none !important; width: 180px; margin: 0 auto 1.5rem; }
    .profile-sidekick { left: -8%; }
    .profile .more-info {
      margin-top: 1.5rem; text-align: center; font-size: 0.85rem;
      /* break out of the 180px block; negative margins, since positioning would re-anchor the sidekick */
      width: calc(100vw - 30px); margin-left: calc(90px - 50vw + 15px);
    }
    .profile .more-info p { display: block; }
  }
</style>

### Hi there 👋

- 🔭 I’m currently working as Head of Knowit Research @ [Knowit](https://www.knowit.no/om-oss/forskning/)
- 🎓 Part-time Lecturer (Universitetslektor) in Software Engineering @ [Department of Informatics, University of Oslo](https://www.mn.uio.no/ifi/?vrtx=person-view&uid=jangu)
- 💼 [CV](/cv/) or [LinkedIn](https://www.linkedin.com/in/janhenrikgundelsby/)
- 🤖 I research how teams and organizations adopt AI agents in software development ([KAIROS](https://www.knowit.no/om-oss/forskning/))
- 💬 Ask me about agentic software engineering, human-AI collaboration, technical debt, platform engineering, and large-scale agile
- 🗣 [Public speaking](/talks/) (in Norwegian)
- 🔬 [Published papers](/publications/)
- 🆔 <a rel="me" href="https://orcid.org/0000-0001-5275-6553">ORCID: 0000-0001-5275-6553</a>
- 📫 How to reach me: [janhenrik@gundelsby.com](mailto:janhenrik@gundelsby.com) or on [LinkedIn](https://www.linkedin.com/in/janhenrikgundelsby/)
- 😄 Pronouns: he/him.
