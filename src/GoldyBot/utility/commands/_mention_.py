from __future__ import annotations
import nextcord
import GoldyBot

GoldyBot_Member = GoldyBot.Member
Nextcord_Member = nextcord.Member

def mention(member:Nextcord_Member|GoldyBot_Member):
    """Fixes slash commands compatibility when mentioning a member the normal way."""

    if isinstance(member, Nextcord_Member):
        return member.mention
    if isinstance(member, GoldyBot_Member):
        return member.member.mention
    else:
        return member